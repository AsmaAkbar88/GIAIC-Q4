# agent as tool
from agents import Agent, Runner , AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig, function_tool
import os
from dotenv import load_dotenv
import asyncio


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")
external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)


# ======================================function tool 
# @function_tool
# async def get_weather(city:str)->str:
#     print("get weather called 2")
#     return f"The weather in {city} is sunny"


# =======================================agent tool 
spanish_agent = Agent(
    name="Spanish agent",
    instructions="you are a translator agent.Your job is to translate the value  into Spanish.",
    model=model,
)

french_agent = Agent(
    name="French agent",
    instructions="you are a translator agent.Your job is to translate the value  into french.",
    model=model,
)

async def main():
    agent = Agent(
        name="main agent",
        instructions="you are a triage_agent 1. if the user ask to translate to spanish use spanish_agent 2. if the user ask to translate to french use french_agent",
        tools=[
            spanish_agent.as_tool(
                tool_name="translate_to_spanish",
                tool_description="answer the user's question in spanish",
            ),
            french_agent.as_tool(
                tool_name="translate_to_french",
                tool_description="answer the user's question in french",
            )
        ],
        
    )
    result = await Runner.run(
        agent, 
        'translate this to french: hello world', 
        run_config=config,
        
    )
    print("Final Response: ",result.final_output)
    print("Last Agent: ",result.last_agent.name) 

if __name__ == "__main__":
    asyncio.run(main())
