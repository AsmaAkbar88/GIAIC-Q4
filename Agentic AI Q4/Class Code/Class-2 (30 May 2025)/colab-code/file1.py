# discord link class:
# https://colab.research.google.com/drive/1dz1lViKhXBJCMyv40zH4pAc90P1LVP-m?usp=sharing 


# =====================================================cell1:
# 🟢 1. Install openai-agents with litellm support
!pip install openai-agents "openai-agents[litellm]"

import nest_asyncio
nest_asyncio.apply()


# ======================================================cell2

# 🟢 2. Main Agent Setup
from google.colab import userdata

API_KEY = userdata.get("GEMINI_API_KEY")
MODEL_NAME = "gemini/gemini-2.0-flash"

from agents import Agent, Runner , set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel 

model = LitellmModel(model=MODEL_NAME, api_key=API_KEY)
set_tracing_disabled (True)

assistant = Agent(
    name="Assistant",
    instructions="You will help with queries",
    model=model
)

# 🟢 4. Async Main
import asyncio

async def main():
    result = await Runner.run(
        starting_agent=assistant,
        input="Hello, how are you?"
    )
    print(result.final_output )


# 🟢 5. Run async loop
asyncio.run( main() )

