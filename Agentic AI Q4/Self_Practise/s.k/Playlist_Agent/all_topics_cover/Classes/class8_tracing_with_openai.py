# s.k code github
# https://github.com/subhankaladi/OpenAI_Agents_SDK/blob/main/00_Internal_working/tracing/Specific_Spans.py
# 🔹  ============ Required Imports ============ 

from agents import OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, Runner, Agent ,set_trace_processors
from agents.tracing.processors import ConsoleSpanExporter , BatchTraceProcessor 
import os
from dotenv import load_dotenv
from agents.tracing.processor_interface import TracingExporter
from agents.tracing.spans import Span
from agents.tracing.traces import Trace


# 🔹  ============ Load Environment Variables ============ 


class CustomConsoleSpanExporter(TracingExporter):
    def export(self, items: list[Trace | Span]):
        for item in items:
            if isinstance(item, Trace):
                print(f"[Trace] ID: {item.trace_id} | Name: {item.name}")
            elif item.span_data.type == "generation":
                usage = item.span_data.usage or {}
                model = item.span_data.model
                user_input = item.span_data.input or []
                output = item.span_data.output or []

                print("🧠 Model Used:", model)
                print("📥 Input Tokens:", usage.get("input_tokens", "N/A"))
                print("📤 Output Tokens:", usage.get("output_tokens", "N/A"))

                if user_input:
                    print("🙋 User Asked:", user_input[-1].get("content", "N/A"))
                if output:
                    print("🤖 Bot Replied:", output[0].get("content", "N/A"))


load_dotenv()
# set_tracing_disabled(True)
# exporter= ConsoleSpanExporter()


exporter= CustomConsoleSpanExporter()         #change this line 
processor = BatchTraceProcessor(exporter)
set_trace_processors([processor])

# 🔹 ============  Gemini API Key ============ 
gemini_api_key = os.getenv("GEMINI_API_KEY")


# 🔹  ============ Provider Setup (AsyncOpenAI) ============ 
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# 🔹  ============ Model Setup ============ 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)



# 🔹  ============ Agent Definition ============ 

agent_one = Agent(
    name="Frontend Expert",
    instructions="you are a forntend expert",
    model=model
)


# 🔹  ============ Run Agent (Sync Mode) ============ 
result = Runner.run_sync(
    agent_one,
    input="Helo how are you",
)
print(result.final_output)


    # ok
    # uv run class8_tracing_with_openai.py