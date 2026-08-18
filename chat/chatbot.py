"""
Manages communication with the LLMs, implementing core logic such as smart routing,
automatic fallback, and exponential backoff retries to ensure system reliability.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

from chat.tools import tools
from chat.chat_prompts import SYSTEM_PROMPT
from chat.recipes_client import search_recipes_in_laravel
from model_gateway import call_model

load_dotenv()

CHAT_MODEL = "openai/gpt-oss-120b"
OPENROUTER_FALLBACK_MODEL = "openai/gpt-oss-120b"

def process_user_message(user_message: str, history: list = None):
    """
    Processes the user message along with conversation history, manages tool calling,
    invokes the search client, and returns the final response.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Adding the history to the message
    if history:
        for chat in history:
            messages.append({"role": "user", "content": chat.user_prompt})
            messages.append({"role": "assistant", "content": chat.response})

    # Adding the user current prompt to the message
    messages.append({"role": "user", "content": user_message})

    response = call_model(
        messages=messages,
        groq_model=CHAT_MODEL,
        openrouter_model=OPENROUTER_FALLBACK_MODEL,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message

    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        
        try:
            function_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            function_args = {}

        if function_name == "search_recipes":
            # connecting to the laravel search recipes client(if the model decided to use the tool)
            db_results = search_recipes_in_laravel(function_args)

            messages.append(response_message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(db_results)
            })

            try:
                second_response = call_model(
                   messages=messages,
                    groq_model=CHAT_MODEL,
                    openrouter_model=OPENROUTER_FALLBACK_MODEL,
                    tool_choice="none",
                )
                
                final_answer = second_response.choices[0].message.content
            except Exception as e:
                final_answer = (
                    "I found some results, but I couldn't find a great match "
                    "for exactly what you're looking for. Could you try "
                    "rephrasing your request or adjusting your filters?"
                )
 
            return {
                "status": "success",
                "response": final_answer
            }
 
    return {
        "status": "success",
        "response": response_message.content
    }