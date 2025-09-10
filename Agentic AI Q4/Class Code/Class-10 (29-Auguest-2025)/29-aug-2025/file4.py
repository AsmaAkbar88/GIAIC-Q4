#   # is_enabled=True

# -------------------- IMPORTS & ENV SETUP --------------------
# Yahan libraries import ho rahi hain aur .env file load ki ja rahi hai
import os  
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, StopAtTools

load_dotenv()


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

def check_admin(admin :  str):
    # Ye function check karta hai ki user admin hai ya nahi
    if admin  == "admin":
        return True
    else:
        return False

@function_tool(
    name_override= "Save_Data_Tool",         # Tool ka naam LLM ke liye override kiya
    description_override= "this fn is saving the data",  # Description override
    # is_enabled=True                        # Always enable tool
    # is_enabled=check_admin ("Umar")             # Admin check ke base par enable
    is_enabled=check_admin ("admin")              # Admin check ke base par enable
)  
def save_data(name: str):
    # Ye tool user ka naam database (dummy) me save karta hai
    return f"Saved data:  {name}" 



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
# >---llm = F.O 
   # is_enabled=check_admin ("Umar")
# I am sorry, I cannot fulfill this request.


#   is_enabled=check_admin ("admin") 
# OK. I have saved your name Umar in the database.


# -------------------- FINAL OUTPUT --------------------
print(result1.final_output)



# OK