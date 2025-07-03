#uv run main.py

import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel , AsyncOpenAI, RunConfig
import asyncio

async def main():
    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise RuntimeError("KEY NOT FOUND")

    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY ,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model= MODEL_NAME ,
        openai_client=external_client
    )


    config = RunConfig(
        model=model,
        model_provider = external_client,
        tracing_disabled = True
    )

    agent = Agent(
        name = "assistant",
        instructions = "you are a helpful assistant",
        model = model
    )

    result = await Runner.run(
        agent,
        "tell me about piaic.",
        run_config = config
    )

    print(result.final_output)



if __name__ == "__main__":
    asyncio.run( main())
   
