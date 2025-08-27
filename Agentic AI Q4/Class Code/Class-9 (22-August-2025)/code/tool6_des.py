
# 🔹============== Required Imports ==============

import os
import asyncio
from dotenv import load_dotenv
from agents import (  Agent,  Runner,  OpenAIChatCompletionsModel,  AsyncOpenAI,  RunConfig, function_tool , ModelSettings)

# 🔹============= Load Environment Variables ==============

load_dotenv()

# 🔹============== Get API Key and Model Name ==============

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

# 🔹============== Check API Key ==============

if not GEMINI_API_KEY:
    raise RuntimeError("KEY NOT FOUND")

# 🔹============== External Client (AsyncOpenAI) ==============

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 🔹============== Model Setup ==============

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client,
)

# 🔹============== Run Configuration ==============

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)
# 🔹============== Function Tool ==============

@function_tool( name_override= "get_weather",description_override= "Return weather info for the specified city")
def f1(city: str):
    """Return weather info for the specified city"""
    return "f The weather in {city} is sunny"

@function_tool
def calculator ():
    """Calculator a mathematical expression and returns the result"""
    return 4 + 4

# 🔹============== Agent (Assistant) Creation ==============

async def main():
    base_agent = Agent(
        name="Base Agent",
        instructions= "You are a helpfull Assistant",
        model=model, 
        tools= [get_weather , calculator],
        model_settings= ModelSettings(tool_choice= "required")
        )
   
 # 🔹============== Runner Execution ==============

    result = await Runner.run(
        base_agent,
        "hello... ??? what is weather of karachi??", 
        run_config=config,
        max_turns= 1
    )

# 🔹============== Print Final Output ==============

    print(result.final_output)


# 🔹============== Script Entry Point ==============

if __name__ == "__main__":
    asyncio.run(main())


# OK