#chainlit run main.py asiy chlna is ko 

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel , RunConfig
import chainlit as cl



#load enviroment variables form .env files
load_dotenv()

#Get Gemini API key from enviroment variable
gemini_api_key = os.getenv( "GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("KEY NOT FOUND")

#Initialize OpenAI Provider (Gemini API URL needs to match your actual endpoint if different)

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)


#Difine the chat completion model
model = OpenAIChatCompletionsModel(
    model="gpt-4.1-nano-2025-04-14",
    openai_client=external_client
)

agent = Agent(
    name="Head Master",
    instructions="you are a helpful assistant",
    model=model
)
config = RunConfig(
    model = model,
    model_provider= external_client,
    tracing_disabled=True
)

#Event: on chat strt
@cl.on_chat_start
async def main():
    await cl.Message("Hello as any things").send()

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message("Thinking. . .").send()
    
    result = Runner.run_sync(agent, message.content , run_config=config)
    await cl.Message(result.final_output).send()

    
    

    