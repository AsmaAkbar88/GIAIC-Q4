# 🎯 Example 3: Time-Based Instructions
# Time-Based: Change behavior based on time of day

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
    print("\n🎭 Example 3: Time-Based Instructions")
    print("-" * 40)
    
    import datetime
    
    def time_based(context: RunContextWrapper, agent: Agent) -> str:
        """Time-based instructions based on current hour."""
        current_hour = datetime.datetime.now().hour
        
        if 6 <= current_hour < 12:
            return f"You are {agent.name}. Good morning! Be energetic and positive."
        elif 12 <= current_hour < 17:
            return f"You are {agent.name}. Good afternoon! Be focused and productive."
        else:
            return f"You are {agent.name}. Good evening! Be calm and helpful."
    
    agent_time = Agent(
        name="Time Aware Agent",
        instructions=time_based,
        model=model
    )
    
    result = Runner.run_sync(agent_time, "How are you today?")
    print("Time-Based Agent:")
    print(result.final_output)

if __name__ == "__main__":
    main()

    # ================================================================================================

# time_based() function →

# Current system ka hour (datetime.now().hour) check karta hai.

# Agar 6–12 baje ke beech hai → "Good morning" message deta hai.

# Agar 12–17 baje ke beech hai → "Good afternoon" message deta hai.

# Warna → "Good evening" message deta hai.

# Saath me agent ka naam add karta hai.

# 📌 Simple me:
# Yeh program ek time-aware AI banata hai jo tumse baat karte waqt
# apni greeting din ke waqt ke hisaab se change karega.