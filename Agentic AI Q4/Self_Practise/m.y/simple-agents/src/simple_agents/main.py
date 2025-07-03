from dotenv import load_dotenv 
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
  

async def agentss(user_input):
    load_dotenv() 
    set_tracing_disabled(True) 

#Provider:
    provider = AsyncOpenAI(     
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
    ) 
 #Model:
    model = OpenAIChatCompletionsModel( 
    model="gemini-2.0-flash-exp", 
    openai_client=provider, 
    ) 
 #Agents:
    Agent1 = Agent( 
    name="Assistant", 
    instructions="you are helpful assistant that solves basic math problem.", 
    model=model 
    ) 
 #Agents_Runner:
    response = Runner.run_sync( 
    starting_agent=Agent1, 
    input = user_input, 
    ) 
 #output:
    return response.final_output