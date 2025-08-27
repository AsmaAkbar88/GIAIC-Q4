
# 🔹============== Required Imports ==============

import os
import asyncio
from dotenv import load_dotenv
from agents import (  Agent,  Runner,  OpenAIChatCompletionsModel,  AsyncOpenAI,  RunConfig)

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

# 🔹============== Agent (Assistant) Creation ==============

async def main():
    base_agent = Agent(
        name="Base Agent",
        instructions= "You are a helpfull Assistant",
        model=model)
    
    creative_Agent = base_agent.clone()

 # 🔹============== Runner Execution ==============


    result = await Runner.run(
        # base_agent,
        creative_Agent,
        "hello hw are you doing..??",
        run_config=config,)

# 🔹============== Print Final Output ==============

    print(result.final_output)


# 🔹============== Script Entry Point ==============

if __name__ == "__main__":
    asyncio.run(main())


# OK