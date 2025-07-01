# cell1:

!pip install openai-agents "openai-agents[litellm]"
!pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()

# cell2
from google.colab import userdata

MODEL_NAME = "gemini/gemini-2.0-flash"
API_KEY = userdata.get("GEMINI_API_KEY")

#cell03:
# 🟢 1. Install openai-agents with litellm support
!pip install openai-agents "openai-agents[litellm]"

# 🟢 2. Colab: Get API key from secrets
from google.colab import userdata

MODEL_NAME = "gemini/gemini-2.0-flash"
API_KEY = userdata.get("GEMINI_API_KEY")

# 🟢 3. Main Agent Setup
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel

model = LitellmModel(model=MODEL_NAME, api_key=API_KEY)

assistant = Agent(
    name="Assistant",
    instructions="You will help with query",
    model=model
)

# 🟢 4. Async Main
import asyncio

async def main():
    result = await Runner.run(
        starting_agent=assistant,
        input="Hello, how are you?"
    )
    print(result.final_output)

# 🟢 5. Run async loop
await main()
