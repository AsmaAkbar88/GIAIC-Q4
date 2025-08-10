from dotenv import load_dotenv
from agents import Agent , Runner ,set_tracing_disabled , OpenAIChatCompletionsModel , function_tool , RunContextWrapper 
from openai import AsyncOpenAI 
from dataclasses import dataclass
import os
import asyncio


load_dotenv()
set_tracing_disabled (True)

provider = AsyncOpenAI(     
    api_key=os.getenv("1st_open_router_api_key"), 
    base_url="https://openrouter.ai/api/v1"
    ) 
 #Model:
model = OpenAIChatCompletionsModel( 
    model="z-ai/glm-4.5-air:free", 
    openai_client=provider, 
    ) 

@dataclass
class UserInfo1:
    name: str
    uid: int
    location: str = "Pakistan"

@function_tool
async def fetch_user_info(wrapper: RunContextWrapper[UserInfo1]) -> str:
    '''Returns the age & name of the user.'''
    return f"User {wrapper.context.name} is 30 years old"

@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo1]) -> str:
    '''Returns the location of the user.'''
    return f"User {wrapper.context.name} is from {wrapper.context.location}"

async def main():
    user_info = UserInfo1(name="Muhammad Qasim", uid=123)

    agent = Agent[UserInfo1](
        name="Assistant",
        instructions= "you are helpfull agent and when you need to use function tool",
        tools=[fetch_user_info,fetch_user_location],
        model=model
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the user's location?",
        context=user_info,
    )

    print(result.final_output)
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main()) 