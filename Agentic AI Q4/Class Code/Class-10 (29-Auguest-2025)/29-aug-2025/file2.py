# "stop_on_first_tool"

# -------------------- IMPORTS & ENV SETUP --------------------
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled

load_dotenv()
# set_tracing_disabled(True)



# -------------------- API KEYS --------------------
# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")



# -------------------- EXTERNAL CLIENT SETUP --------------------
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)



# -------------------- MODEL SETUP --------------------
model_gemni = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)



# -------------------- TOOLS --------------------
@function_tool
def fetch_data():
    return {
        "name": "hamza",
        "age": 20
    }

@function_tool
def save_data(name: str):                      #  new line
    return f"Saved data:  {name}"

# -------------------- AGENT --------------------
starting_agent = Agent(
    name="Data Manager",
    model=model_gemni,
    tools=[fetch_data, save_data],
    tool_use_behavior="stop_on_first_tool"    
)

# -------------------- RUNNER EXECUTION --------------------
result1 = Runner.run_sync(starting_agent, "hello, save my name in the database. My name is Hamza")  
# --> Saved data: Hamza

result2 = Runner.run_sync(starting_agent, """hello, Please fetch user data and 
                         save my name in the database. My name is Hamza""")  
# -->  {'name': 'hamza', 'age': 20}

# -------------------- FINAL OUTPUT --------------------
print(f"Final_Output1:    {result1.final_output}")
print(f"Final_Output2:    {result2.final_output}")


# ok