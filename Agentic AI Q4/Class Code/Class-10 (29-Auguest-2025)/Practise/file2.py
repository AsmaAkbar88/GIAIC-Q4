# github code 
# https://github.com/panaversity/learn-agentic-ai/blob/main/01_ai_agents_first/15_advanced_tools/tools_masterclass/part2.py


import os
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, MaxTurnsExceeded, set_tracing_disabled

load_dotenv()
set_tracing_disabled(True)

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

gemini_api_key: str = os.getenv("GEMINI_API_KEY")

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
def get_weather(city: str) -> str:
    return f"Sunny"

base_agent: Agent = Agent(
    name="Weather_Agent",
      model=llm_model,
        tools=[get_weather]
        )

# print(f"Tool:  {base_agent.tools}")

async def main():
    try:
        res = await Runner.run(base_agent, "What is weather in Lahore", max_turns=2)
        print(f"Final_OUTPUT:   {res.final_output}")
    except MaxTurnsExceeded as e:
        print(f"Max turns exceeded: {e}")

if __name__ == "__main__":
    asyncio.run(main())

    # ok