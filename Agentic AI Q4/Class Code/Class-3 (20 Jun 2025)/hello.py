# 📌🔹============  Import Libraries ============
import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner , set_tracing_disabled
import asyncio

# 📌🔹============  Main Function ============
async def main():
    # ✅ Load Environment Variables
    load_dotenv()
    set_tracing_disabled(True)

    # ✅ 🔹============ API Key & Model Setup ============
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise ValueError("KEY NOT FOUND")

    # ✅🔹============  External Client Setup ============
    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY ,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # ✅🔹============  Model Setup ============
    model = OpenAIChatCompletionsModel(
        model= MODEL_NAME ,
        openai_client=external_client
    )

    # ✅🔹============ Agent Creation ============
    teacher = Agent(
        name = "Math Teacher",
        instructions = "you are a Math Teacher",
        model = model
    )

    # ✅🔹============ Run Agent ============
    result = await Runner.run(
        starting_agent= teacher,
        input = "tell me the answer of 10 * 10 ."
    )

    # ✅🔹============ Print Final Output ============
    print(result.final_output)

# 📌🔹============ Entry Point  ============
if __name__ == "__main__":
    asyncio.run(main())


# ok
# uv run hello.py