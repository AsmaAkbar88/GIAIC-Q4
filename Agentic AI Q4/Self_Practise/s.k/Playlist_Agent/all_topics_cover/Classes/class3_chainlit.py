# 🔹 ============== Required Imports============== 
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Runner, Agent
import os
from dotenv import load_dotenv
import chainlit as cl


# 🔹 ============== Load Environment Variables============== 
load_dotenv()


# 🔹 ============== Gemini API Key============== 
gemini_api_key = os.getenv("GEMINI_API_KEY")


# 🔹 ============== Provider Setup (AsyncOpenAI)============== 
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# 🔹 ============== Model Setup============== 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)


# 🔹 ============== Run Configuration============== 
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)


# 🔹 ============== Agent Definition============== 
agent_one = Agent(
    name="Frontend Expert",
    instructions="you are a forntend expert",
)


# 🔹 ============== Chat Start Event============== 
@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Hello from Aasma Akbar.").send()


# 🔹 ============== On Message Event============== 
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})
    
    result = await Runner.run(
        agent_one,
        input=history,
        run_config=config
    )
    
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    await cl.Message(content=result.final_output).send()
