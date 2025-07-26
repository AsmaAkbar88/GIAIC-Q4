import asyncio
from agents import Agent , Runner  , AsyncOpenAI , RunConfig , OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv
import os

load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("KEY NOT FOUND")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
        model=model,
        model_provider = external_client,
        tracing_disabled = True
    )

@function_tool
async def get_weather(city: str) -> str:
    """ a function that returns the weather in a given city"""
    print("get weather is callws")
    return f'The Weather in {city} is soo good' ,


french_agent = Agent(
    name="french_agent",
    instructions="You are a helpful French agent that translates French.",
    handoff_description="You are a helpfull french agent.",
)
    

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You are a helpful Spanish agent that translates Spanish.",
    handoff_description="You are a helpfull spanish agent",
)

triage_agent = Agent(
    name="triage_agent",
    instructions="You are a triage agent. Based on the user request, hand off to the correct language agent.",
    handoffs=[spanish_agent, french_agent],
    tools= [get_weather]
   
)

async def main():
    result = await Runner.run( triage_agent , 'tell me the weatther of karachi, and "hello" in french language' ,run_config= config)
    print("Final Response:  "  , result.final_output )
    print("Last Agent:  " , result.last_agent.name )


if __name__ == "__main__":
    asyncio.run(main())

    