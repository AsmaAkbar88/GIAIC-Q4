# Github link
# https://github.com/syeda-hoorain-ali/giaic-q3/tree/main/class-16

import os
from agents import (
    Agent, RunContextWrapper, Runner, StopAtTools, function_tool, 
    set_default_openai_api, set_default_openai_client, set_tracing_disabled
)
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI


load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("Enviroment variable 'GEMINI_API_KEY' is not set.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_default_openai_client(external_client)
set_tracing_disabled(disabled=True)
set_default_openai_api("chat_completions")


# ===========================================================
# ==================== tool_use_behavior ====================
# ===========================================================

# Simple tools
@function_tool
def fetch_data1():
    return { "name": "hamzah", "age": 24 }

@function_tool
def save_data1():
    return "Saved data"


# Create agent
agent1 = Agent(
    name="Data Manager",
    tools=[fetch_data1, save_data1],
    model="gemini-2.0-flash",
    tool_use_behavior="stop_on_first_tool", # default "run_llm_again"
)

result1 = Runner.run_sync(
    starting_agent=agent1,
    # input="hello, fetch user data for me"
    # input="fetch user data and save it in the database"
    input="save my name is the database: my name is hamzah"
)

print(result1.final_output)


# =====================================================
# ==================== StopAtTools ====================
# =====================================================

# Simple tools
@function_tool
def fetch_data2():
    return { "name": "hamzah", "age": 24 }

@function_tool
def save_data2():
    return "Saved data"


# Create agent
agent2 = Agent(
    name="Data Manager",
    tools=[fetch_data2, save_data2],
    model="gemini-2.0-flash",
    tool_use_behavior=StopAtTools(stop_at_tool_names=["fetch_data"])
)

result2 = Runner.run_sync(
    starting_agent=agent2,
    # input="hello, fetch user data for me"
    # input="fetch user data and save it in the database"
    input="save my name is the database: my name is hamzah"
)

print(result2.final_output)



# =========================================================================================
# ==================== name_override, description_override, is_enabled ====================
# =========================================================================================

# Simple tools
@function_tool
def fetch_data3():
    return { "name": "hamzah", "age": 24 }

@function_tool(
    name_override="save_user_data", 
    description_override="this fn is saving user data",
    is_enabled=False,
)
def save_data3():
    """this function is saving data"""
    return "Saved data"


# Create agent
agent3 = Agent(
    name="Data Manager",
    tools=[fetch_data3, save_data3],
    model="gemini-2.0-flash",
    tool_use_behavior=StopAtTools(stop_at_tool_names=["fetch_data"])
)

result3 = Runner.run_sync(
    starting_agent=agent3,
    input="save my name is the database: my name is hamzah"
)

print(result3.final_output)




# ============================================================
# ==================== Dynamic is_enabled ====================
# ============================================================

# Simple tools
@function_tool
def fetch_data4():
    return { "name": "hamzah", "age": 24 }

def check_is_admin4():
    return False

@function_tool(
    name_override="save_user_data", 
    description_override="this fn is saving user data",
    is_enabled=check_is_admin4(),
)
def save_data4():
    """this function is saving data"""
    return "Saved data"



# Create agent
agent4 = Agent(
    name="Data Manager",
    tools=[fetch_data4, save_data4],
    model="gemini-2.0-flash",
    tool_use_behavior=StopAtTools(stop_at_tool_names=["fetch_data"])
)

result4 = Runner.run_sync(
    starting_agent=agent4,
    input="save my name is the database: my name is hamzah"
)

print(result4.final_output)



# ================================================================
# ==================== failure_error_function ====================
# ================================================================

# Simple tools
@function_tool
def fetch_data5():
    return { "name": "hamzah", "age": 24 }

def check_is_admin():
    return False

def error_handler(context: RunContextWrapper, error: Exception):
    # Send mail or msg on whatsapp
    print("email sent")
    return "Error handeled"

@function_tool(
    failure_error_function=error_handler
)
def save_data5():
    """this function is saving data"""
    raise Exception("Error saving data")
    return "Saved data"



# Create agent
agent5 = Agent(
    name="Data Manager",
    tools=[fetch_data5, save_data5],
    model="gemini-2.0-flash",
    tool_use_behavior=StopAtTools(stop_at_tool_names=["fetch_data"])
)

result5 = Runner.run_sync(
    starting_agent=agent5,
    input="save my name is the database: my name is hamzah"
)

print(result5.final_output)