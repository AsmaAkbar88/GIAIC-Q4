#uv run tool.py

# discord link class:
# https://discord.com/channels/1352950461883482172/1376559198623760474/1386663301206900890

# ===============================
# 📌 Imports
# ===============================
import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, function_tool
import asyncio


# ===============================
# 📌  Tool Definition
# ===============================
@function_tool
def get_weather(city):
    """This is a weather tool"""
    return f"The weather of {city} is moderated"


# ===============================
# 📌 Main Function
# ===============================
async def main():
    load_dotenv()

    # 🔑🔹============  Load API Key  =========== 
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise ValueError("KEY NOT FOUND")

    # 🌐🔹============  External Client Setup🔹 ========== 
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # 🤖🔹============  Model Setup =========== 
    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    # 🧑‍💻🔹============  Agent Setup =========== 
    assistant = Agent(
        name="Weather Assistant",
        instructions="Your task is to provide weather details of the specific city",
        model=model,
        tools=[get_weather]
    )
    
    # ▶️🔹============  Run Agent =========== 
    result = await Runner.run(
        starting_agent=assistant,
        input="tell me the weather of karachi"
    )

    print(result.final_output)


# ===============================
# 📌 Entry Point
# ===============================
if __name__ == "__main__":
    asyncio.run(main())

   
# ok