#uv run main.py

import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner 
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

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


    teacher = Agent(
        name = "Math Teacher",
        instructions = "you are a Math Teacher",
        model = model
    )

    result = Runner.run_sync(
        starting_agent= teacher,
        input = "tell me the answer of 10 * 10 ."
    )
    print(result.final)
    

if __name__ == "__main__":
    asyncio.run( main())
   
