import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel

load_dotenv()

api_key = os.getenv( "OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("KEY NOT FOUND")

model = OpenAIChatCompletionsModel(
    model="gpt-4.1-nano-2025-04-14",
    openai_client=api_key
)
Agent = Agent(
    name="assistant",
    instructions="you are a helpful assistant"
)

result = Runner.run_sync(Agent, "Who is the founder of Pakistan?")
print(result.final_output)
