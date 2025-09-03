# 🔹 ============== Required Imports ============== 
from agents import( OpenAIChatCompletionsModel, 
                   AsyncOpenAI, RunConfig, Runner, Agent ,
                   input_guardrail, GuardrailFunctionOutput,
                    InputGuardrailTripwireTriggered)
import os
from dotenv import load_dotenv
import chainlit as cl
from pydantic import BaseModel

# 🔹 ============== Load Environment Variables ============== 
load_dotenv()


# 🔹 ============== Gemini API Key ============== 
gemini_api_key = os.getenv("GEMINI_API_KEY")


# 🔹 ============== Provider Setup (AsyncOpenAI) ============== 
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# 🔹 ============== Model Setup ============== 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)


# 🔹 ============== Run Configuration ============== 
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# 🔹 ========== Guardrail Base Class ==========
class Output_python(BaseModel):
    is_python_related : bool
    reasoning: str

# 🔹 ========== Guardrail Agent ==========
input_gurdrails_agent = Agent(
    name = "Input Gurdrails Checker",
    instructions = "Check if the user's question is related to Python programming. if it is, return true,if it is not,return false.",
    model= model,
    output_type= Output_python
)
@input_guardrail
async def input_gurdrail_fun(ctx , agent , input):
    result = await Runner.run(input_gurdrails_agent, input)

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered=not result.final_output.is_python_related
    )


# 🔹 ============== Agent Definition============== 
agent_one = Agent(
    name="PythonExpert",
    instructions="You are a Python expert. Only respond to Python programming questions.",
    model=model,
    input_guardrails= [input_gurdrail_fun]
)


# 🔹 ============== Chat Start Event============== 
@cl.on_chat_start
async def handle_start_chat():
  await cl.Message(content="👋 I’m a Python Expert Assistant. Ask me anything about Python programming!").send()


# 🔹 ============== On Message Event============== 

# @cl.on_message
# async def main(mess : cl.Message):
#    result = await Runner.run(
#       agent_one,
#       input = mess.content
#    )
#    await cl.Message(content= result.final_output).send()
#   ye sirf python ka reply dy rha hy koi error through nhi kr rha 

# ==========================================================

@cl.on_message
async def main(message: cl.Message):
    try:
        result = await Runner.run(
            agent_one,
            input=message.content
        )
        await cl.Message(content=result.final_output).send()

    except InputGuardrailTripwireTriggered:
        await cl.Message(content="⚠️ Sorry, Please try python related question.").send()


# ok
# uv run chainlit run class5_input_gurdrails.py -w