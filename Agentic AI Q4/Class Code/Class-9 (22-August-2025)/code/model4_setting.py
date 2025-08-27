# github class link:
#     https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/07_model_settings


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

@function_tool
def get_weather (city: str):
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
        # model_settings= ModelSettings(tool_choice= "auto")   # The weather in Karachi is sunny.
        # model_settings= ModelSettings(tool_choice= "required") # I'm doing great, thanks for asking! I just checked the weather in London and it's sunny. How can I help you today?
        model_settings= ModelSettings(tool_choice= "none")      # none
        )
   

 # 🔹============== Runner Execution ==============

    result = await Runner.run(
        base_agent,
        # "hello... ??? what is weather of karachi??",       # ------------> auto
        # "hello... ??? hw are you??",                       # ------------> required
        " what is weather of karachi??" ,                    # --------------> none
        run_config=config,
    )

# 🔹============== Print Final Output ==============

    print(result.final_output)


# 🔹============== Script Entry Point ==============

if __name__ == "__main__":
    asyncio.run(main())


# OK