 # 🎯 Example 5: Exploring Context and Agent

import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunContextWrapper

# 🌿================= Load environment variables =================
load_dotenv()
set_tracing_disabled(True)

# 🔐================= Setup Gemini client =================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

def main():
    print("\n🎭 Example 5: Exploring Context and Agent")
    print("-" * 40)
    
    def explore_context_and_agent(context: RunContextWrapper, agent: Agent) -> str:
        """Explore what's available in context and agent."""
        # Access conversation messages
        messages = getattr(context, 'messages', [])
        message_count = len(messages)
        
        # Access agent properties
        agent_name = agent.name
        tool_count = len(agent.tools)
        
        return f"""You are {agent_name} with {tool_count} tools. 
        This is message #{message_count} in our conversation.
        Be helpful and informative!"""
    
    agent_explorer = Agent(
        name="Context Explorer",
        instructions=explore_context_and_agent,
        model=model
    )
    
    result = Runner.run_sync(agent_explorer, "What can you tell me about yourself?")
    print("Context Explorer Agent:")
    print(result.final_output)
    
    print("\n🎉 You've learned Dynamic Instructions!")
    print("💡 Try changing the functions and see what happens!")

if __name__ == "__main__":
    main()

# ========================================================================================

# Ek explore_context_and_agent function banata hai jo:

# Conversation ka message count nikalta hai

# Agent ka naam aur tools ka count check karta hai

# Inko instruction ke roop me return karta hai.

# Ek Agent banata hai jo yeh function har request pe chalata hai.

# "What can you tell me about yourself?" input ke saath run karke output print karta hai.

# Basically: yeh example tumhe dikhata hai ke agent ke andar se tum context (chat ka history)
# aur agent ke properties  access karke dynamic instructions bana sakte ho.