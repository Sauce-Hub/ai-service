---


## AI Part Roles

The AI has 3 main roles:

1. **Recipe Extraction**  
   Extract ingredients from the user's prompt and return them in JSON format to the backend.

2. **Recipe Explanation**  
   Explain the recipe returned by the backend in a simple and user-friendly way.

3. **Nutrition & Time Calculation**  
   Calculate nutrition facts and estimated cooking time when requested by the user.

## LLM used: 

- **GPT-OSS-120B** 
- for nutrition and calculation-related tasks, and for user interaction, recipe extraction, and tool calling.

## Libraries used : 

**FastAPI**   To create the API and endpoints for the AI service.
**Uvicorn**      To run the FastAPI server.
**Requests**      To send HTTP requests and communicate with other APIs or services.
**python-dotenv** To load environment variables from the .env file, such as API keys.
**Pydantic**      To define and validate the structure of input and output data.
**Groq**          To interact with LLMs through the Groq API.
**OpenAI**       To interact with OpenAI or OpenAI-compatible APIs and models.  
You can install all the libraries used from the **requirements.txt** file 

## Core Pipeline
User Input: Sent from the mobile app to the FastAPI backend.

LLM Routing: Tasks are split between Llama (interaction/tools) and GPT (calculations).

Structured Output: Forces clean JSON responses for seamless backend handling.

Fallback: Automatically switches to backup models if errors or rate limits occur.   

## Repo Structure : 
- We have three main parts in this repo :
- 1. chat folder : for handling the chatting logic, sending filters and delivering the recipes details.
  2. Nutrition calculation folder : for calculating the nutrition facts for each added recipe.
  3. main file : for running the project.
  4. model_gateway : for calling the models and fallback system. 
