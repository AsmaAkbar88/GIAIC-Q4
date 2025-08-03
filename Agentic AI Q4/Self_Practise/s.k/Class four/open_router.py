from dotenv import load_dotenv 
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
  

load_dotenv() 
set_tracing_disabled(True) 

#Provider:
provider = AsyncOpenAI(     
    api_key=os.getenv("1st_open_router_api_key"), 
    base_url="https://openrouter.ai/api/v1"
    ) 
 #Model:
model = OpenAIChatCompletionsModel( 
    model="openrouter/horizon-beta", 
    openai_client=provider, 
    ) 
 #Agents:
agent1 = Agent( 
    name="Assistant", 
    instructions="you are helpful assistant.", 
    model=model 
    ) 
 #Agents_Runner:
response = Runner.run_sync( 
    starting_agent=agent1, 
    input = "Who is the founder of pakistan and 5 line his personilty easy english", 
    ) 
 #output:
print(response.final_output)