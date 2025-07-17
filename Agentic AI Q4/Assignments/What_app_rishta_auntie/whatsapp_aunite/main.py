from agents import Agent ,AsyncOpenAI , OpenAIChatCompletionsModel ,  Runner
import os
from dotenv import load_dotenv


load_dotenv()  # This will load the .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
MODEL_NAME = "gemini-2.0-flash"

if not GEMINI_API_KEY:
    raise ValueError("KEY NOT FOUND")

external_client = AsyncOpenAI(
 api_key = GEMINI_API_KEY ,
 base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client= external_client ,
    model= MODEL_NAME 
)

agent = Agent(
    name = "Aunite",
    model= model
)

result = Runner.run_sync(
    starting_agent= agent,
    input= "hello"
)
print(result.final_output)