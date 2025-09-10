# github link 
# https://github.com/panaversity/learn-agentic-ai/blob/main/01_ai_agents_first/15_advanced_tools/tools_masterclass/part4.py


import os
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool

load_dotenv()

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
# (description_override="", failure_error_function=)
def get_weather(city: str) -> str:
        # Dummy service call (replace with real API later)
    if city == "lahore":
        return "🌞 It's hot and sunny in Lahore today!"
    else:
        return f"⛅ Weather info for {city} is not available, assume it's clear."
 


base_agent: Agent = Agent(name="WeatherAgent", instructions="" ,model=llm_model, tools=[get_weather])

async def main():
    res = await Runner.run(base_agent, "What is weather in Lahore")
    print(res.final_output)

if __name__ == "__main__":
    asyncio.run(main())

    # ok