# -------------------- IMPORTS & ENV SETUP --------------------
# Yahan libraries import ho rahi hain aur .env file load ki ja rahi hai
import os  
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, StopAtTools ,set_tracing_disabled 


load_dotenv()
# set_tracing_disabled(True)    

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
def erro_handler(ctx , error: Exception):    #---------------------- new line
    print("Sent Email")
    return "Error Hnadled"

@function_tool(failure_error_function=erro_handler)

def save_data(name: str):
   raise Exception ("Error saving data") # --> llm--> tool--> error = F.O

   return "Savingdata"



# -------------------- AGENT --------------------
starting_agent = Agent(
    name="Data Manager",
    model= model_gemni,
    tools=[fetch_data, save_data],
    tool_use_behavior = StopAtTools(stop_at_tool_names= ["save_data"]) 
    # 👉 Matlab: jaise hi "save_data" call hogi, process yahan ruk jayega
    
)


# -------------------- RUNNER EXECUTION --------------------
result1 = Runner.run_sync(starting_agent, "Please save my name Umar in the database.")



# -------------------- FINAL OUTPUT --------------------
print(result1.final_output)


# OUTPUT: 
# Sent Email
# Error Hnadled

# OK