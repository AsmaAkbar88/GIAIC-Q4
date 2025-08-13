
from dotenv import load_dotenv
from agents import (
    Agent,   Runner,  set_tracing_disabled,  OpenAIChatCompletionsModel,  function_tool, RunContextWrapper)
from openai import AsyncOpenAI
from dataclasses import dataclass
import asyncio
import os


# --------------------Environment & Setup  --------------------

load_dotenv()
set_tracing_disabled(True)

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# --------------------Model Configuration --------------------

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# --------------------User Context Dataclass------------------

@dataclass
class UserInfo1:
    name: str
    uid: int
    location: str = "Pakistan"

# --------------------Function Tools------------------

@function_tool
async def fetch_user_info(wrapper: RunContextWrapper[UserInfo1]) -> str:
    """Return a short description about the user (example tool)."""
    return f"User {wrapper.context.name} (id: {wrapper.context.uid}) is 30 years old."


@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo1]) -> str:
    """Return the user's location from the run context."""
    return f"User {wrapper.context.name} is from {wrapper.context.location}."


#  --------------------Main runner --------------------

async def main() -> None:
    #  --------------------Create user context --------------------
    user_info = UserInfo1(name="Muhammad Qasim", uid=123)

    #  --------------------Initialize agent with tools --------------------
    agent = Agent[UserInfo1](
        name="Assistant",
        instructions=(
            "You are a helpful assistant. When appropriate, call the provided function tools"
            " to retrieve user information such as age and location."
        ),
        tools=[fetch_user_info, fetch_user_location],
        model=model,
    )

    #  --------------------Run the agent --------------------
    result = await Runner.run(
        starting_agent=agent,
        input="hello?",
        context=user_info,
    )

    #  --------------------Print outputs --------------------
    print("Final output:\n", result.final_output)

#  --------------------Entry point --------------------

if __name__ == "__main__":
    asyncio.run(main())
