#learn-agentic-ai/01_ai_agents_first/06_chatbot/chatbot/main.py



from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner 
import asyncio
import chainlit as cl
import os
load_dotenv()

@cl.on_chat_start

async def start():   
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise ValueError("KEY NOT FOUND")

    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY ,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model= MODEL_NAME ,
        openai_client=external_client
    )

    cl.user_session.set("chat_history", [])
    teacher = Agent(
        name = "Math Teacher",
        instructions = "you are a Math Teacher",
        model = model
    )
    cl.user_session.set("agent" , teacher)
    
    await cl.Message(content="Welcome to Friday Class...! How can I help you today?").send()

    # 2nd step ============================

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    teacher = cl.user_session.get("agent") 
    history = cl.user_session.get("chat_history")

    history.append({"role": "user", "content": message.content})

    result = await Runner.run(
    starting_agent= teacher,
    input = history
    )

    msg.content = result.final_output
    await msg.update()
    cl.user_session.set("chat_history" , result.to_input_list())

    print(result.final_output)

# if __name__ == "__main__":   # chainlit chala rhi ho tu is code ki zrort nhi hy 
#     asyncio.run(start())
   
