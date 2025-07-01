import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel , AsyncOpenAI, RunConfig

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("KEY NOT FOUND")

external_client = AsyncOpenAI(
    api_key = api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name = "assistant",
    instructions = "you are a helpful assistant",
    model = model
)

result = Runner.run_sync(
    agent,
    "tell me about piaic.",
    run_config = config
)

print(result.final_output)
