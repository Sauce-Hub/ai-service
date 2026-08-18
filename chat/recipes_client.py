
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Mock function for the recipe search service in laravel
LARAVEL_SEARCH_URL = os.getenv("LARAVEL_SEARCH_URL")
LARAVEL_API_KEY = os.getenv("LARAVEL_API_KEY")

def search_recipes_in_laravel(filters: dict) -> list:
    """
   Connects to the laravel server to send the filters and take the recipes found
    """
    headers = {
        "X-API-KEY": LARAVEL_API_KEY
    }
    try:
        response = requests.post(LARAVEL_SEARCH_URL, params=filters, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Laravel backend: {e}")
        return []