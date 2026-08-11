"""
Defines the tools and function schemas available to the LLM, 
instructing the model on how to structure outputs and extract parameters for database queries.
"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_recipes",
            "description": (
                "Search the recipes database using the given filters. "
                "Use this tool ONLY when the user is asking for a recipe "
                "recommendation or wants to find a dish based on ingredients, "
                "category, cooking time, or nutritional goals."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "include_ingredients": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": "Ingredients that must be present. MUST be singular form (e.g., 'egg' not 'eggs', 'flour' not 'flours')."
                    },
                    "exclude_ingredients": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                        "description": (
                            "List of specific ingredient names that must NOT be present "
                            "in the recipe. MUST be singular form. ALWAYS expand general terms "
                            "(e.g., instead of 'dairy', exclude 'milk', 'cheese', 'butter')."
                        )
                    },
                    "category": {
                        "type": ["string", "null"],
                        "enum": ["breakfast", "lunch", "dinner", None],
                        "description": "The category of the meal matching the database categories."
                    },
                    "max_estimated_time": {
                        "type": ["string", "null"],
                        "description": "Maximum estimated preparation time (e.g., '30 minutes')."
                    },
                    "min_carbs": {
                        "type": ["number", "null"],
                        "description": "Minimum carbs required. MUST be a raw numeric value, NEVER a string."
                    },
                    "max_calories": {
                        "type": ["number", "null"],
                        "description": "Maximum calories limit. MUST be a raw numeric value, NEVER a string."
                    },
                    "min_protein": {
                        "type": ["number", "null"],
                        "description": "Minimum protein required. MUST be a raw numeric value, NEVER a string."
                    },
                    "max_protein": {
                        "type": ["number", "null"],
                        "description": "Maximum protein limit. MUST be a raw numeric value, NEVER a string."
                    },
                    "min_fats": {
                        "type": ["number", "null"],
                        "description": "Minimum fats required. MUST be a raw numeric value, NEVER a string."
                    },
                    "max_fats": {
                        "type": ["number", "null"],
                        "description": "Maximum fats limit. MUST be a raw numeric value, NEVER a string."
                    },
                    "min_calories": {
                        "type": ["number", "null"],
                        "description": "Minimum calories limit. MUST be a raw numeric value, NEVER a string."
                    },
                    "max_carbs": {
                        "type": ["number", "null"],
                        "description": "Maximum carbs limit. MUST be a raw numeric value, NEVER a string."
                    }
                }
            }
        }
    }
]