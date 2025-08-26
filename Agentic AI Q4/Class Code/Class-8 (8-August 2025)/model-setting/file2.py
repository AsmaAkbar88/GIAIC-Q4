import os
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool, ModelSettings, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

# 🌿 Load environment variables from .env file
load_dotenv()

# 🚫 Disable tracing for clean output (optional for beginners)
set_tracing_disabled(disabled=True)

# 🔐 1) Environment & Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # 🔑 Get your API key from environment
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"  # 🌐 Gemini-compatible base URL (set this in .env file)

# 🌐 Initialize the AsyncOpenAI-compatible client with Gemini details
external_client: AsyncOpenAI = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

# 🧠 2) Model Initialization
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# 🛠️ Simple tool for learning
@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of a rectangle."""
    area = length * width
    return f"Area = {length} × {width} = {area} square units"

def main():
      # 🎯 Example 2: Tool Choice
    print("\n🔧 Tool Choice Settings")
    print("-" * 30)
    
    # Agent can decide when to use tools (default)
    agent_auto = Agent(
        name="Auto",
        tools=[calculate_area],
        model_settings=ModelSettings(tool_choice="auto"),
        model=model
    )
    
    # Agent MUST use a tool (even if not needed)
    agent_required = Agent(
        name="Required",
        tools=[calculate_area],
        model_settings=ModelSettings(tool_choice="required"),
        model=model
    )

# Agent CANNOT use tools (chat only)
    agent_none = Agent(
        name="None",
        tools=[calculate_area],
        model_settings=ModelSettings(tool_choice="none"),
        model=model
    )
    
    question = "What's the area of a 5x3 rectangle?"
    
    print("1: ---- Auto Tool Choice: ----")
    result_auto = Runner.run_sync(agent_auto, question)
    print(result_auto.final_output)
    
    print("\n2: ---- Required Tool Choice: ----")
    result_required = Runner.run_sync(agent_required, question)
    print(result_required.final_output)

    print("\n3: ---- None Tool Choice: ----")
    result_none = Runner.run_sync(agent_none, question)
    print(result_none.final_output)
    
    print("\n💡 Notice: Auto = decides, Required = must use tool")

if __name__ == "__main__":
    main()