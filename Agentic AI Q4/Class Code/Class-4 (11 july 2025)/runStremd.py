# discord class link:
# GitHub Repository: https://github.com/syeda-hoorain-ali/giaic-q3/tree/main/class-10

# ===============================
# 📌 Imports
# ===============================
import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner 
from openai.types.responses import ResponseTextDeltaEvent
import asyncio


# ===============================
# 📌 Main Function
# ===============================
async def main():
    load_dotenv()

    # 🔑 Load API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise ValueError("KEY NOT FOUND")

    # 🌐 External Client Setup
    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY ,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # 🤖 Model Setup
    model = OpenAIChatCompletionsModel(
        model= MODEL_NAME ,
        openai_client=external_client
    )

    # 👨‍🏫 Agent Setup
    agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model)

    # ▶️ Run Streamed Agent
    result = Runner.run_streamed(
        starting_agent= agent,
        input = "tell me something interesting about pakistan in 100 words"
    )

    # 📡 Stream Events
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance (
            event.data, ResponseTextDeltaEvent
        ):
            print(event.data.delta, end='', flush=True)


# ===============================
# 📌 Entry Point
# ===============================
if __name__ == "__main__":
    asyncio.run( main())

# ok