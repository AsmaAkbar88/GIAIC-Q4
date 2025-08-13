 # 🎯 Example 4: Stateful Instructions (Remembers)
# Stateful: Remember interactions and adapt accordingly

import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunContextWrapper

# 🌿================= Load environment variables  =================
load_dotenv()
set_tracing_disabled(True)

# 🔐 ================= Setup Gemini client =================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

def main():
    print("\n🎭 Example 4: Stateful Instructions")
    print("-" * 40)
    
    class StatefulInstructions:
        """Stateful instructions that remember interaction count."""
        def __init__(self):
            self.interaction_count = 0
        
        def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
            self.interaction_count += 1
            
            if self.interaction_count == 1:
                return "You are a learning assistant. This is our first interaction - be welcoming!"
            elif self.interaction_count <= 3:
                return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
            else:
                return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient."
    
    instruction_gen = StatefulInstructions()
    
    agent_stateful = Agent(
        name="Stateful Agent",
        instructions=instruction_gen,
        model=model
    )
    
    # ================= Test multiple interactions =================
    for i in range(3):
        result = Runner.run_sync(agent_stateful, f"Question {i+1}: Tell me about AI")
        print(f"Interaction {i+1}:")
        print(result.final_output[:100] + "...")
        print()


if __name__ == "__main__":
    main()

# ==========================================================================================

# StatefulInstructions ek class hai jo interaction ka count (interaction_count) track karti hai.

# Jab pehli dafa call hota hai → friendly welcome message deta hai.

# Agli 2–3 dafa → pehle wale conversation pe build karta hai.

# Uske baad → efficient ho jaata hai aur concise answer deta hai.

# __call__ method har interaction pe instructions dynamically banata hai.

# For loop 3 dafa agent se question karta hai taake change dikh sake.

# Yani yeh dynamic instructions + memory ka example hai.
