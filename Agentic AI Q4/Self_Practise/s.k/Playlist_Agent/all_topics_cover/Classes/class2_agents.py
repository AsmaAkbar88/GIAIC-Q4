# 🔹  ============ Required Imports ============ 
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Runner, Agent
import os
from dotenv import load_dotenv


# 🔹  ============ Load Environment Variables ============ 
load_dotenv()


# 🔹 ============  Gemini API Key ============ 
gemini_api_key = os.getenv("GEMINI_API_KEY")


# 🔹  ============ Provider Setup (AsyncOpenAI) ============ 
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# 🔹  ============ Model Setup ============ 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)


# 🔹  ============ Run Configuration ============ 
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)


# 🔹  ============ Agent Definition ============ 
agent_one = Agent(
    name="Frontend Expert",
    instructions="you are a forntend expert",
)


# 🔹  ============ Run Agent (Sync Mode) ============ 
result = Runner.run_sync(
    agent_one,
    input="Helo how are you",
    run_config=config
)


# 🔹  ============ Print Final Output ============ 
print(result.final_output)
