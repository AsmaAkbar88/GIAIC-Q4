# github link 
# https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/19_agent_lifecycle

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
    AgentHooks
)
from dataclasses import dataclass
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
@dataclass
class Order:
    order_id : str
    customer_name: str
    amount: float


# 🔹============== Agent Hooks ==============
class SimpleAgentHook(AgentHooks):
    async def on_start(self, context: RunContextWrapper, agent: Agent):
        """This agent is starting"""
        print(f"[Start] Agent '{agent.name}' started")

    async def on_end(self, context: RunContextWrapper, agent: Agent, result):
        """This agent finished"""
        print(f"[End] Agent '{agent.name}' finished. result : {result}")

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent ,tool):
        """This agent is using a tool"""
        print(f"[TOOL Start] Agent '{agent.name}' is using a tool.")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool , result):
        """This agent finished using a tool"""
        print(f"[TOOL End] Tool '{tool.name}' done. Result: {result} ")


# 🔹============== Simple Tool ==============
@function_tool
def refund_order(wrapper: RunContextWrapper[Order]):
    """Process a refund for the customer order"""
    print("[TOOL EXECUTION] refund_order tool is being executed!")
    order = wrapper.context
    return f"Refund of ${order.amount} processed for Order {order.order_id }  customer '{order.customer_name}'"


# 🔹============== Run Configuration ==============
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

my_hooks = SimpleAgentHook()


# 🔹============== Agent (Assistant) Creation ==============
async def main():
    support_agent = Agent(
        name="Support Bot",
        instructions=(
            "You are a customer support agent. "
            "You must use the refund_order tool to process refunds.\n"
            "Important: Always call the refund_order tool when someone asks about a refund. "
            "Do not just say you'll process it — actually use the tool."
        ),
        model=model,
        tools=[refund_order],
        hooks=my_hooks,
    )

    print("=" * 50)
    print("Agent Hooks Demo")
    print("=" * 50)

    # 🔹============== Runner Execution ==============

    order = Order("ID8877788" , "Johan" , 909009)
    result = await Runner.run(
        support_agent,
        "i need a refund for my order . Please process my refund now",
        run_config=config,
        context= order
    )

    # 🔹============== Print Final Output ==============
    print(result.final_output)


# 🔹============== Script Entry Point ==============
if __name__ == "__main__":
    asyncio.run(main())


# OK