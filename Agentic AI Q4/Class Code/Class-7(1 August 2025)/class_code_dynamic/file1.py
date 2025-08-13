# 🎭 Dynamic Instructions: Make Your Agent Adapt
# Simple examples to learn dynamic instructions

import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunContextWrapper

# 🌿 =================Load environment variables=================
load_dotenv()
set_tracing_disabled(True)


# 🔐 =================Setup Gemini client=================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)


def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 1: Basic Dynamic Instructions
    print("\n🎭 Example 1: Basic Dynamic Instructions")
    print("-" * 40)
    
    def basic_dynamic(context: RunContextWrapper, agent: Agent) -> str:
        """Basic dynamic instructions function."""
        return f"You are {agent.name}. Be helpful and friendly."
    
    agent_basic = Agent(
        name="Dynamic Agent",
        instructions=basic_dynamic,
        model=model
    )
    
    result = Runner.run_sync(agent_basic, "hello!")
    print("Basic Dynamic Agent:")
    print(result.final_output)
    

if __name__ == "__main__":
    main()

# ==================================================================================

# Dynamic Instructions ka matlab hai: agent ki instructions fix na ho, balki runtime
# pe function se banengi.

# Yahan basic_dynamic function har bar agent ka naam le kar ek friendly prompt banata hai.

# Jab agent run hota hai (Runner.run_sync), ye function call hota hai aur us waqt
# ki instructions agent ko di jaati hain.

# Short mein — ye code agent ko har run pe adaptable behavior deta hai instead 
# of fixed system prompt.
