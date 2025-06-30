import chainlit as cl
from multi_agents.main import agent
import asyncio

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
    content="Welcome to the Multi-Agent System! How can I assist you today?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    response = asyncio.run(agent(user_input))
    await cl.Message(
    content=f"{response}"
    ).send()