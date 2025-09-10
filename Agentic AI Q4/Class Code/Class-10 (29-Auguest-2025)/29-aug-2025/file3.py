# StopAtTools(stop_at_tool_names= ["save_data]"]) 

# -------------------- IMPORTS & ENV SETUP --------------------
# Yahan libraries import ho rahi hain aur .env file load ki ja rahi hai
import os  
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, StopAtTools, set_tracing_disabled

load_dotenv()
set_tracing_disabled(True)


# -------------------- API KEYS --------------------
# Yahan OpenAI aur Gemini dono ke API keys environment se li ja rahi hain
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
gemini_api_key= os.getenv("GEMINI_API_KEY")



# -------------------- EXTERNAL CLIENT SETUP --------------------
# Gemini ko OpenAI-style client ke through connect karna
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)



# -------------------- MODEL SETUP --------------------
# Gemini model ko agent ke liye ready karna
model_gemni = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)



# -------------------- TOOLS --------------------
@function_tool
def fetch_data():
    return  {
        "name" : "hamza",
        "age"  : 20
    }

@function_tool
def save_data(name: str):
    return f"Saved data:  {name}" 



# -------------------- AGENT --------------------
starting_agent = Agent(
    name="Data Manager",
    model= model_gemni,
    tools=[fetch_data, save_data],
    tool_use_behavior = StopAtTools(stop_at_tool_names= ["save_data]"]) 
    # 👉 Matlab: jaise hi "save_data" call hogi, process yahan ruk jayega
    
)



# -------------------- RUNNER EXECUTION --------------------
result1 = Runner.run_sync(starting_agent, "hello, save my name in the database. My name is umar ") 
# -- llm -> tool-> llm = final_output
# OK. I have saved your name (umar) in the database.

result2 = Runner.run_sync(starting_agent, "Please first fetch the user data, then save my name Umar in the database.") 
# I have first fetched the user data and then saved your name Umar in the database.
# -- llm -> tool-> llm = final_output

result3 = Runner.run_sync(starting_agent, "hello, fetch user data for me") 
# I can fetch data for you, but I need a name to save the data under. Could you please provide one?
# -- llm -> tool-> llm = final_output


"""👉 Matlab: jaise hi agent fetch_data call karega → 
woh ruk jayega, aur uske baad save_data nahi chalega."""

# -------------------- FINAL OUTPUT --------------------
# print(result1.final_output)
# print(result2.final_output)
print(result3.final_output)



# OK