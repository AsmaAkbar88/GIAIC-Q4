#uv run main.py

import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner ,function_tool
import asyncio


@function_tool
def get_weather (city):
    """this is a weather tool"""
    return f"The weather of {city} is moderated"

async def main():
    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise ValueError("KEY NOT FOUND")

    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY ,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model= MODEL_NAME ,
        openai_client=external_client
    )


    assistant = Agent(
        name = "Weather Assistant",
        instructions = "you task is to provide of the weather deatils of the specific city",
        model = model,
        tools=[get_weather]
    )

    result = await Runner.run(
        starting_agent= assistant,
        input = "tell me the weather of karachi"
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run( main())
   
