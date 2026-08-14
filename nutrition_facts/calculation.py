"""
Estimates nutritional values ​​(calories, protein, carbs, fat)
and the approximate preparation time for any new recipe,
using a model (gpt-oss-120b) distinct from the chatbot.

Ingredients may be provided in various units (grams, cups, tablespoons/teaspoons, count),
and the model itself converts these units into approximate gram measurements.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

from nutrition_facts.nutri_prompts import NUTRITION_SYSTEM_PROMPT

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

NUTRITION_MODEL = "openai/gpt-oss-120b"


def analyze_recipe(ingredients: list[dict], instructions: str) -> dict:
    """
    takes: 
    - ingredients: [{"name": "flour", "quantity": 1, "unit": "cup"},
                     {"name": "eggs", "quantity": 2, "unit": "count"},
                     {"name": "milk", "quantity": 250, "unit": "g"}, ...]
    - instructions: the recipe steps

   returns dict with :
    {
        "calories": ...,
        "protein_g": ...,
        "carbs_g": ...,
        "fat_g": ...,
        "estimated_time_minutes": ...   
    }
    """

    ingredients_text = "\n".join(
        f"- {item['name']}: {item['quantity']} {item['unit']}"
        for item in ingredients
    )

    user_message = (
        f"Ingredients:\n{ingredients_text}\n\n"
        f"Preparation instructions:\n{instructions}"
    )

    response = client.chat.completions.create(
        model=NUTRITION_MODEL,
        messages=[
            {"role": "system", "content": NUTRITION_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
    )

    raw_content = response.choices[0].message.content
    result = _parse_model_output(raw_content)
    result["estimated_time_minutes"] = _normalize_time(
        result.get("estimated_time_minutes")
    )

    return result


def _parse_model_output(raw_content: str) -> dict:
    """ 
    Converts the model's response into a dictionary
    if that fails, it returns empty values ​​instead of crashing
    """
    try:
        cleaned = (
            raw_content.strip()
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )
        return json.loads(cleaned)
    except (json.JSONDecodeError, AttributeError):
        return {
            "calories": None,
            "protein_g": None,
            "carbs_g": None,
            "fat_g": None,
            "estimated_time_minutes": None,
            "error": "failed to parse model output",
        }


def _normalize_time(value) -> int | None:
    """
   It ensures that (estimated_time_minutes) always returns an integer,
    even if the model errs and returns text, a decimal, or a range (like "20-30")
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return round(value)

    if isinstance(value, str):
        # if the model returned a range (20-30) it returns the first value
        digits = "".join(ch if ch.isdigit() else " " for ch in value)
        numbers = [int(n) for n in digits.split()]
        if numbers:
            return numbers[0]

    return None