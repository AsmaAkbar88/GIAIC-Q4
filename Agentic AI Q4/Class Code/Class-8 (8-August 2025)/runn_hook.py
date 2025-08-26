# discord class link
# https://discord.com/channels/1352950461883482172/1376559198623760474/1403486953101594624


# github link
# https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/20_run_lifecycle

# 🔹============== Required Imports ==============
import os
import asyncio
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    RunConfig,
    function_tool,
    RunContextWrapper,
    RunHooks
)

# 🔹============= Load Environment Variables ==============
load_dotenv()

# 🔹============== Get API Key and Model Name ==============
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

# 🔹============== Check API Key ==============
if not GEMINI_API_KEY:
    raise RuntimeError("KEY NOT FOUND")

# 🔹============== External Client (AsyncOpenAI) ==============
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 🔹============== Model Setup ==============
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client,
)


# 🔹============== Data Class ==============
class Order:
    customer_name: str
    amount: float


# 🔹============== Runner Hooks ==============
class MyRunnerHooks(RunHooks):
    async def on_agent_start(self, context ,agent ):
        print(f"[Runner]:  Agent '{agent.name}' started on Runner Hook")


    async def on_agent_end(self, context, agent, output):
        print(f"[Runner Hooks End]:  Agent '{agent.name}' finished On Runner Hook. Output: '{output}'")


    async def on_tool_start(self, context, agent ,tool):
        print(f"[Runner Hooks on TOOL Start]: Agent  '{agent.name}'  is using a tool '{tool.name}'.")


    async def on_tool_end(self, context, agent, tool , result):
        print(f"[Runner Hooks on TOOL End]:  Agent  '{agent.name}' , Tool: '{tool.name}' ")
        print("[Runner Result:] " , result)


# 🔹============== Simple Tool ==============
@function_tool
def check_order():
    """check order status"""
    return "order #123 is on the way"


@function_tool
def check_refund():
    """check refund status"""
    return "refund of $40 processed!"


# 🔹============== Run Configuration ==============
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

runner_hooks = MyRunnerHooks()


# 🔹============== Agent (Assistant) Creation ==============
async def main():
    agent1 = Agent(
        name="Order Agent",
        instructions="Check Order status",
        model=model,
        tools=[check_order],
        
    )

    agent2 = Agent(
        name="Refund Agent",
        instructions="Check refund status",
        model=model,
        tools=[check_refund],
       
    )

    print("=" * 50)
    print("Runner Hooks Demo")
    print("=" * 50 )

    # 🔹============== Runner Execution Agent 1 ==============
    print()
    print( "=" * 10 , "Checking order", "=" * 10)
    result1 = await Runner.run(
        agent1,
        "check my order",
        run_config=config,
        hooks=runner_hooks,
    )
    # print()
    # print("=" * 10 ,"Refund Order" , "=" * 10)
    # result2 = await Runner.run(
    #     agent2,
    #     "check my refund",
    #     run_config=config,
    #     hooks=runner_hooks,
    # )


    # 🔹============== Print Final Output ==============
    print(f"Answer1: {result1.final_output}")
    # print(f"Answer2: {result2.final_output}")

    
# 🔹============== Script Entry Point ==============
if __name__ == "__main__":
    asyncio.run(main())


    # Ok