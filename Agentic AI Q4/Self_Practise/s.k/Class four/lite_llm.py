# uv add litellm
from dotenv import load_dotenv 
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
from agents.extensions.models.litellm_model import LitellmModel
  

load_dotenv() 
set_tracing_disabled(True) 

gemini_api_key=os.getenv("GEMINI_API_KEY")
model = "gemini/gemini-2.0-flash"
# litellm khta hy tm bas meri class use kro or tmhy baseurl ki bhi need nhi hy


 #Agents:
agent1 = Agent( 
    name="Assistant", 
    instructions="you are helpful assistant.", 
    model= LitellmModel (
        api_key= gemini_api_key,
        model= model) )


 #Agents_Runner:
response = Runner.run_sync( 
    starting_agent=agent1, 
    input = "Who is the founder of pakistan and 5 line his personilty easy english", 
    ) 
 #output:
print(response.final_output)
