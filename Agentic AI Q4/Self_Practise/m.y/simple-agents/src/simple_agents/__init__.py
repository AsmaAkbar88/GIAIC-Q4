from dotenv import load_dotenv 
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
  
#   uv run python src/simple_agents/__init__.py ye aisy run ho gi


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
agent1 = Agent(  
    name="Assistant", 
    instructions="you are helpful assistant that solves basic math problem.", 
    model=model 
) 
 #Agents_Runner:
response = Runner.run_sync( 
    starting_agent=agent1, 
    input = "please tell me 60 +89 + 45 ", 
) 
 #output:
print(response.final_output)