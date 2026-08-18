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