# github linked
# https://github.com/MuzaffarAli13/Youtube--Rishty-wali-Auntie

# 🔹============== Required Imports==============
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel , AsyncOpenAI, RunConfig , function_tool
import chainlit as cl
from whatapp import send_whatsapp_message

# 🔹============= Load Environment Variables ==============
load_dotenv()

# 🔹============== Main Async Function ============== 
 
# 🔹============== Get API Key and Model Name  ==============
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
model_name = "gemini-2.5-flash"
   
# 🔹============== Check API Key ==============
if not GEMINI_API_KEY:
        raise RuntimeError("KEY NOT FOUND")

# 🔹============== External Client (AsyncOpenAI) ==============
external_client = AsyncOpenAI(
    api_key = GEMINI_API_KEY ,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

    # 🔹============== Model Setup ==============
model = OpenAIChatCompletionsModel(
    model= model_name,
    openai_client=external_client
)

# 🔹============== Run Configuration ==============
config = RunConfig(
    model=model,
    model_provider= external_client,
    tracing_disabled=True
)
     # 🔹============== Function Tool ==============

@function_tool
def get_user_data(min_age: int) -> list[dict]:
    "Retrieve user data based on a minimum age"
    users = [
        {"name": "Muneeb", "age": 22},
        {"name": "Muhammad Ubaid Hussain", "age": 25},
        {"name": "Azan", "age": 19},
    ]

    for user in users:
        if user["age"] < min_age:
            users.remove(user)
    
    return users

    # 🔹============== Rishty wali Auntie Agent ==============

raishty_wali = Agent(
    name="Rishtay wali",
    instructions="""
      You are Rishtay Wali Auntie. Find matches from a custom tool based on age only.
      Reply short and send WhatsApp message only if user
        asks behave like a auntie and talk in roman urdu""",
    model=model, 
    tools = [get_user_data , send_whatsapp_message]
)

   # 🔹============== Chainlit ==============
@cl.on_chat_start
async def start():
    cl.user_session.set("history",[])
    await cl.Message("Salam beta! Main Rishty Wali Auntie hoon. Apna rishta batain, age batain, aur WhatsApp number dein. 😄").send()


# Runner
@cl.on_message
async def main(message:cl.Message):
    await cl.Message("Thinking...").send() 
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})

     # 🔹============== Runner Execution ==============

    result = Runner.run_sync(
          starting_agent= raishty_wali,
          input= history
        )
    
    
    history.append({"role": "assistant", "content": result.final_output})
    
    cl.user_session.set("history",history)

    await cl.Message(content=result.final_output).send() 
    


# ok