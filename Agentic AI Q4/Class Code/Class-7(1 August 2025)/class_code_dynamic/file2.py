 # 🎯 Example 2: Context-Aware Instructions
# Context-Aware: Adapt based on conversation history

import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunContextWrapper

# 🌿 =================Load environment variables=================
load_dotenv()
set_tracing_disabled(True)


# 🔐================= Setup Gemini client=================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)


def main():
    print("\n🎭 Example 2: Context-Aware Instructions")
    print("-" * 40)
    
    def context_aware(context: RunContextWrapper, agent: Agent) -> str:
        """Context-aware instructions based on message count."""
        message_count = len(getattr(context, 'messages', []))
        
        if message_count == 0:
            return "You are a welcoming assistant. Introduce yourself!"
        elif message_count < 3:
            return "You are a helpful assistant. Be encouraging and detailed."
        else:
            return "You are an experienced assistant. Be concise but thorough."
    
    agent_context = Agent(
        name="Context Aware Agent",
        instructions=context_aware,
        model=model
    )
    
    # Test with multiple messages
    result1 = Runner.run_sync(agent_context, "hello")
    print("First message:")
    print(result1.final_output)
    
    result2 = Runner.run_sync(agent_context, "Tell me about Python")
    print("\nSecond message:")
    print(result2.final_output)

    
if __name__ == "__main__":
    main()

# ======================================================================================

# context_aware function context check karta hai — specifically kitne messages ho chuke hain 
# (message_count).

# Message count ke basis pe agent ka style badal diya jata hai:

# 0 messages: Agent friendly welcome karega.

# 1-2 messages: Agent detailed aur encouraging hoga.

# 3+ messages: Agent concise lekin thorough hoga.

# Jab aap Runner.run_sync se message bhejte ho, har bar ye function dubara
#  run hota hai aur instructions us waqt ki situation ke mutabiq ban jaati hain.

# Short mein — ye agent apna behavior conversation ke phase ke hisaab se change karta hai.
