"""
Acts as the entry point of the application, configuring and running the FastAPI server,
defining the endpoints, and handling incoming HTTP requests from the frontend or mobile app.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from chatbot import process_user_message

app = FastAPI()

class ChatMessage(BaseModel):
    user_prompt: str
    response: str

class UserRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []



# Simulation of laravel backend search API

@app.post("/api/recipes/search")
def mock_laravel_recipe_search(filters: Dict[str, Any]):
    print("--- [Laravel Mock API] Received Filters from AI:", filters)
    
    mock_recipes = [
        {
            "receipt_id": 1,
            "name": "Oatmeal with Berries",
            "category": "breakfast",
            "Calories": 250,
            "Protein": 8,
            "Carbs": 45,
            "Fats": 4,
            "estimated_time": "15 minutes"
        },
        {
            "receipt_id": 2,
            "name": "Scrambled Eggs with Potato",
            "category": "breakfast",
            "Calories": 320,
            "Protein": 18,
            "Carbs": 25,
            "Fats": 14,
            "estimated_time": "10 minutes"
        }
    ]
    
    return mock_recipes

# AI chat endpoint 

@app.post("/api/ai/chat")
def handle_ai_chat(request: UserRequest):
    try:
        result = process_user_message(request.message, request.history)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))