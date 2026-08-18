"""
Handling model calling and server errors:
1. Retry with exponential backoff for each provider
2. Distinguishing error types (401: not worth retrying; 429/5xx: worth retrying)
3. Fallback with two providers (Groq → OpenRouter) and the same model

"""

import os
import time
import logging
from groq import Groq
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MAX_RETRIES = 2                        
INITIAL_DELAY = 2                     
RETRIABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _try_provider(client, model_name: str, kwargs: dict, provider_name: str):
    """
Attempts to execute the request on a single provider only, using smart retries
and returns the response upon success, or `None` if the provider fails completely
(whether after exhausting all retry attempts or due to an error that doesn't worth a retry)
"""
    for attempt in range(MAX_RETRIES + 1):
        try:
            logger.info(f"[{provider_name}] Attempt {attempt + 1} using {model_name}")
            return client.chat.completions.create(model=model_name, **kwargs)

        except Exception as e:
            status_code = getattr(e, "status_code", None)

            
            # 401 : the key is wrong or canceled so retring won't help so it goes to the other provider
           
            if status_code == 401:
                logger.error(
                    f"[{provider_name}] Unauthorized (401). "
                    f"Check the API key. Skipping retries for this provider."
                )
                return None
            
            # Temporary errors (rate limit / server errors) or network errors
            # (status_code is usually None in case of timeout/connection error)
            # -> Worth retrying
            
            if status_code in RETRIABLE_STATUS_CODES or status_code is None:
                if attempt < MAX_RETRIES:
                    delay = INITIAL_DELAY * (2 ** attempt)
                    logger.warning(
                        f"[{provider_name}] Attempt {attempt + 1} failed "
                        f"(status={status_code}): {e}. Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"[{provider_name}] Retries exhausted.")
                    return None

            # Any other error not covered above (e.g: 400 Bad Request)
            # No use in retrying on the same provider
            
            logger.error(f"[{provider_name}] Non-retriable error (status={status_code}): {e}")
            return None

    return None


def call_model(
    messages: list,
    groq_model: str,
    openrouter_model: str,
    tools: list | None = None,
    tool_choice: str | None = None,
    temperature: float = 0.7,
):
    """
    The single entry point that chatbot.py and calculation.py call
    """

    kwargs = {"messages": messages, "temperature": temperature }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice or "auto"

    providers = [
        ("Groq", groq_client, groq_model),
        ("OpenRouter", openrouter_client, openrouter_model),
    ]

    for provider_name, client, model_name in providers:
        result = _try_provider(client, model_name, kwargs, provider_name)
        if result is not None:
            return result

    raise RuntimeError("All providers failed for this request. Check logs above for details.")