#  ye simple chainlit ka code hy 

from dotenv import load_dotenv 
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
import chainlit as cl
  

load_dotenv() 
set_tracing_disabled(True) 

#Provider:
provider = AsyncOpenAI(     
api_key=os.getenv("GEMINI_API_KEY"), 
base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
) 

 #Model:
model = OpenAIChatCompletionsModel( 
model="gemini-2.0-flash", 
openai_client=provider, 
) 

 #Agents:
agent1 = Agent( 
name="Assistant", 
instructions="you are helpful assistant.", 
model=model 
) 


@cl.on_message
async def handle_message(message : cl.Message):
    response = await Runner.run( 
        starting_agent = agent1,
         input = message.content)
    
 #output:
    await cl.Message(content= response.final_output).send()

