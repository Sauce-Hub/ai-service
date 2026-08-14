---
noteId: "7f80e75095cb11f198d1c70358a5dd75"
tags: []

---


## AI Part Roles

The AI has 3 main roles:

1. **Recipe Extraction**  
   Extract ingredients from the user's prompt and return them in JSON format to the backend.

2. **Recipe Explanation**  
   Explain the recipe returned by the backend in a simple and user-friendly way.

3. **Nutrition & Time Calculation**  
   Calculate nutrition facts and estimated cooking time when requested by the user.

## LLMs

- **Llama 3.3 70B Versatile:** Used for user interaction, recipe extraction, and tool calling.
- **GPT-OSS-120B:** Used mainly for nutrition and calculation-related tasks.

## Core Pipeline
User Input: Sent from the mobile app to the FastAPI backend.

LLM Routing: Tasks are split between Llama (interaction/tools) and GPT (calculations).

Structured Output: Forces clean JSON responses for seamless backend handling.

Fallback: Automatically switches to backup models if errors or rate limits occur.
