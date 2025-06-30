import chainlit as cl
from simple_agents.main import agentss
@cl.on_chat_start
async def chat_start():
    await cl.Message(content="Welcome ").send()


@cl.on_message
async def main(message : cl.Message):
    reply = await agentss (message.content)
    await cl.Message (content= reply).send()
    
    
# aisy likh lo ya waisy bt 1 hi hy 
# @cl.on_message
# async def main(mes : cl.Message):
#     uer = mes.content
#     reply = await pora (uer)
#     await cl.Message (content= reply).send()
    