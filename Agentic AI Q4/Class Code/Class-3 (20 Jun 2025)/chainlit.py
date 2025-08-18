#learn-agentic-ai/01_ai_agents_first/06_chatbot/chatbot/main.py

# discord link class:
# https://discord.com/channels/1352950461883482172/1376559198623760474/1385944200759083098

# ======================================================
# 📌 Chatbot using Chainlit + OpenAI Agents SDK + Gemini
# ======================================================

from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner 
import chainlit as cl
import os

# 🔑 Load Environment Variables
load_dotenv()


# ======================================================
# 🚀 On Chat Start
# ======================================================
@cl.on_chat_start
async def start():   
    # API Key & Model
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
    MODEL_NAME = "gemini-2.0-flash"

    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY NOT FOUND")

    # 🔗 Connect Gemini with OpenAI wrapper
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # 🎯 Model Selection
    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    # 📝 User Session (store history & agent)
    cl.user_session.set("chat_history", [])

    teacher = Agent(
        name="Math Teacher",
        instructions="You are a Math Teacher",
        model=model
    )
    cl.user_session.set("agent", teacher)
    
    # 👋 Welcome Message
    await cl.Message(content="👋 Welcome to Friday Class...! How can I help you today?").send()



# ======================================================
# 💬 On User Message
# ======================================================
@cl.on_message
async def main(message: cl.Message):
    # Thinking message
    msg = cl.Message(content="🤔 Thinking...")
    await msg.send()

    # Get agent & history from session
    teacher = cl.user_session.get("agent") 
    history = cl.user_session.get("chat_history")

    # Append new user message
    history.append({"role": "user", "content": message.content})

    # Run the Agent
    result = await Runner.run(
        starting_agent=teacher,
        input=history
    )

    # Show Final Answer
    msg.content = result.final_output
    await msg.update()

    # Save Updated History
    cl.user_session.set("chat_history", result.to_input_list())

    # Debug Print
    print(result.final_output)

# if __name__ == "__main__":   # chainlit chala rhi ho tu is code ki zrort nhi hy 
#     asyncio.run(start())
   

#    ok
#  uv run chainlit run chainlit.py -w
