# ========== Imports ==========

from dotenv import load_dotenv
from agents import (
    Agent,  Runner, set_tracing_disabled,  OpenAIChatCompletionsModel, RunContextWrapper
)
from openai import AsyncOpenAI
from dataclasses import dataclass
import asyncio
import os


# ==========  Environment Setup  ========== 

load_dotenv()
set_tracing_disabled(True)


# ==========  Provider Configuration  ========== 

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#  ==========  Model Setup  ========== 

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

#  ==========  User Data Class ========== 
@dataclass
class UserInfo1:
    name: str
    uid: int
    location: str = "Pakistan"


#  ==========  Dynamic Instructions Function  ========== 

def dynamic_instructions(context: RunContextWrapper, agent: Agent) -> str:
    print("DEBUG: Agent name is ->", agent.name) # DEBUG: Agent name is -> Smart Assistant
    return f"You are {agent.name}. Adapt to the user's needs."
#  ==========  Main Async Function =========== 

async def main():

    #  ========== Create user context ========== 

    user_info = UserInfo1(name="Muhammad Qasim", uid=123)

    #  ========== Initialize Agent ========== 

    agent =  Agent(
        name=f"{user_info.name}'s Smart Assistant",
        instructions=dynamic_instructions , # ✅ Changes based on context
        model=model
    )

    #  ========== Run the agent ========== 

    result = await Runner.run(
        starting_agent=agent,
        input="salam, hello can you helpp me ",
        context=user_info,
    )

    #  ========== Display results ========== 

    print(result.final_output)
    print("Last agent:", result.last_agent.name)


# ===== Entry Point =====

if __name__ == "__main__":
    asyncio.run(main())
