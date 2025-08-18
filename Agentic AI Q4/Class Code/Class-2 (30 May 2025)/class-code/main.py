#uv run main.py

# Gemini API Key:
# To generate your Gemini API Key go to https://makersuite.google.com/app

# discord link class:
# https://discord.com/channels/1352950461883482172/1376559198623760474/1378292126953111682

# uv run main.py


# 🔹============== Required Imports==============
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel , AsyncOpenAI, RunConfig
import asyncio

# 🔹============= Load Environment Variables ==============
load_dotenv()

# 🔹============== Main Async Function ==============
async def main():  
 
    # 🔹============== Get API Key and Model Name  ==============
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    # 🔹============== Check API Key ==============
    if not GEMINI_API_KEY:
        raise RuntimeError("KEY NOT FOUND")

    # 🔹============== External Client (AsyncOpenAI) ==============
    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY ,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # 🔹============== Model Setup ==============
    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    # 🔹============== Run Configuration ==============
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # 🔹============== Agent (Assistant) Creation ==============
    assistant = Agent(
        name="Assistant",
        instructions="Your job is to resolve queries",
        # model=model
    )

    # 🔹============== Runner Execution ==============
    result = await Runner.run(
        assistant,
        "tell me something interesting about Pakistan..",
        run_config = config
    )

    # 🔹============== Print Final Output ==============
    print(result.final_output)

# 🔹============== Script Entry Point ==============
if __name__ == "__main__":
    asyncio.run( main())


# ok