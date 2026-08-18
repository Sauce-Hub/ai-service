"""
Acts as the entry point of the application, configuring and running the FastAPI server,
defining the endpoints, and handling incoming HTTP requests from the frontend or mobile app.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.responses import JSONResponse

from chat.chatbot import process_user_message
from nutrition_facts.calculation import analyze_recipe
app = FastAPI()

class ChatMessage(BaseModel):
    user_prompt: str
    response: str

class UserRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class IngredientItem(BaseModel):
    name: str
    quantity: float
    unit: str   


class NutritionRequest(BaseModel):
    ingredients: List[IngredientItem]
    instructions: str

# Simulation of laravel backend search API

@app.get("/api/recipes/search")
def mock_laravel_recipe_search(filters: Dict[str, Any]):
    print("--- [Laravel Mock API] Received Filters from AI:", filters)
    mock_recipes = [
            {
                "receipt_id": 1,
                "name": "Pasta",
                "caption": "Quick and delicious pasta",
                "category": "DINNER",
                "estimated_time_min": 20,
                "calories": 300,
                "fats": 15,
                "carbs": 70,
                "protein": 20,
                "timestamp": "2026-08-10T18:00:00Z",
                "user": {
                    "user_id": 1,
                    "name": "Ahmed"
                },
                "ingredients": [
                    {
                        "id": 1,
                        "name": "Pasta",
                        "quantity": 200,
                        "unit": "g",
                        "isAssigned": False
                    },
                    {
                        "id": 2,
                        "name": "Tomato Sauce",
                        "quantity": 100,
                        "unit": "g",
                        "isAssigned": False
                    }
                ],
                "instructions": "1. Boil water in a large pot with a pinch of salt.    2. Add 200g of pasta and cook for 10 to 12 minutes until tender.    3. Drain the pasta and mix it thoroughly with warm tomato sauce.    4. Serve hot and enjoy your quick dinner."
            }
        ]
    return mock_recipes

# AI chat endpoint 

@app.post("/api/ai/chat")
def handle_ai_chat(request: UserRequest):
    try:
        ai_result = process_user_message(request.message, request.history)
        return ai_result 

    except Exception as e:
        err_msg = str(e).lower()
        
        if "429" in err_msg or "rate limit" in err_msg or "quota" in err_msg:
            message = "You are out of tokens, try again later."
            status_code = 429
        elif "401" in err_msg:
            message = "Invalid API key."
            status_code = 401
        else:
            message = f"An unexpected error occurred: {str(e)}"  
            status_code = 500
            
        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "response": message}
        )

#AI nutrition calculation endpoint

@app.post("/api/ai/calculate-nutrition")
def handle_nutrition_calculation(request: NutritionRequest):
    try:
        ingredients = [item.model_dump() for item in request.ingredients]
        result = analyze_recipe(ingredients, request.instructions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))