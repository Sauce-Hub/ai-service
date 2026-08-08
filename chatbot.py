"""
Manages communication with the LLMs, implementing core logic such as smart routing,
automatic fallback, and exponential backoff retries to ensure system reliability.
"""
##  testing the apis
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
models_to_test = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b"
]
for model_name in models_to_test:
    print(f"\n{'='*50}")
    print(f"model is : {model_name}")
    print('='*50)
    try : 
            completion = client.chat.completions.create(
            model=model_name,
            messages=[
            {
            "role": "user",
            "content": "tell me an easy recipe with eggs and no diary"
            }
            ],
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
            )

            for chunk in completion:
              print(chunk.choices[0].delta.content or "", end="")
            print()
    except Exception as e :
        print("an error occured")