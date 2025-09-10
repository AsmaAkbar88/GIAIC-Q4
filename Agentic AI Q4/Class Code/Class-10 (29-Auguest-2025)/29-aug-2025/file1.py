# "stop_on_first_tool"
# discord_class_link
# https://discord.com/channels/1352950461883482172/1376559198623760474/1411105767016108072

# ------------------------------1. Required Imports & Setup------------------------------
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled



# ------------------------------Load environment variables from .env file------------------------------
load_dotenv()
# set_tracing_disabled(True)   # Only for tracing disable (optional)



# .------------------------------ API Keys Setup------------------------------
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY", "")



#  ------------------------------External Client (Gemini API)------------------------------
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")



# ------------------------------ 4. Model Configuration------------------------------
model_gemni = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)



#----------------------------- Function Tools------------------------------
@function_tool
def fetch_data():
    """Fake function to fetch user data"""
    return {
        "name": "hamza",
        "age": 20
    }

@function_tool
def save_data():
    """Fake function to save user data"""
    return "Saved data"


#------------------------------ Agent Setup------------------------------
starting_agent = Agent(
    name="Data Manager",
    model=model_gemni,
    tools=[fetch_data, save_data],
    tool_use_behavior="stop_on_first_tool"   # Behavior of tool usage
)

#  ---------------------------Runner Execution------------------------------
# Step 01 → Only fetch user data (single tool call)
result1 = Runner.run_sync(
    starting_agent,
    "hello, Please fetch user data for me"
)
# Final_Output1: {'name': 'Hamza', 'age': 20}



# Step 02 → Fetch user data + Save it in database (multiple tool calls)
result2 = Runner.run_sync(
    starting_agent,
    "hello, Please fetch user data and Save it in the database: Hamzah"
)
# Final_Output2: {'name': 'Hamza', 'age': 20}


# Step 03 → Only save_data (single tool call)
result3 = Runner.run_sync(
    starting_agent,
    "Please save my data into the database."
)
# Final_Output3:    Saved data





#------------------------------ Final Output Results------------------------------
print(f"Final_Output1:    {result1.final_output}")
print(f"Final_Output2:    {result2.final_output}")
print(f"Final_Output3:    {result3.final_output}")


# ok


