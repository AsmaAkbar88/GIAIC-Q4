# 🔹 ============== Required Imports ============== 
from agents import (OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Runner, Agent ,
                     input_guardrail , output_guardrail ,
                      GuardrailFunctionOutput, 
                      InputGuardrailTripwireTriggered ,OutputGuardrailTripwireTriggered)
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


# 🔹 ============== Run Configuration============== 
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)


# 🔹 ==========Input Guardrail Base Class ==========
class Output_python(BaseModel):
    is_python_related : bool
    reasoning: str


# 🔹 ==========Input Guardrail Agent ==========
input_gurdrails_agent = Agent(
    name = "Input Gurdrails Checker",
    instructions = """Check if the user's question is related to Python programming. 
                      Only return true if it is about Python.""",
    model= model,
    output_type= Output_python
)


# 🔹 ==========Input Guardrail Agent Fun ==========
@input_guardrail
async def input_gurdrail_fun(ctx , agent , input):
    print(f"Input Gurdrails:  " , input)
    result = await Runner.run(input_gurdrails_agent, input)

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered=not result.final_output.is_python_related
    )

# 🔹 ==========Onput Guardrail Base Class ==========
class MessageOutput(BaseModel): 
    response: str

class PythonOutput(BaseModel): 
    reasoning: str
    is_python: bool
   

# 🔹 ==========Output Guardrail Agent ==========
output_gurdrails_agent = Agent(
    name = "Onput Gurdrails Checker",
    instructions ="You are a strict classifier. Check if the response is about Python programming. "  ,      
    model= model,
    output_type= PythonOutput
)


# 🔹 ==========output Guardrail Agent Fun ==========
@output_guardrail
async def output_gurdrail_fun(ctx , agent , output: MessageOutput):

    result = await Runner.run(output_gurdrails_agent, output)

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        # tripwire_triggered=result.final_output.is_python #last line chal rhi hy (block)
        tripwire_triggered=not result.final_output.is_python #agr python sy related swl hy tu wo jwb day ga
    )

# 👉 is line ki wajah se jab Python sawal hota hai aur is_python=True hota hai to tumne usko not 
# karke False banadiya. isliye answer dikh jata hai ✅ (ye part sahi hai).
# Lekin agar guardrail ne galti se is_python=False diya to wo not 
# False = True hojata hai aur block ho jata hai 🔴."""



# 🔹 ============== Agent Definition============== 
agent_one = Agent(
    name="PythonExpert",
    instructions="You are a Python expert. Only respond to Python programming questions.",
    model=model,
    input_guardrails= [input_gurdrail_fun],
    output_guardrails= [output_gurdrail_fun]
)


# 🔹 ============== Chat Start Event============== 
@cl.on_chat_start
async def handle_start_chat():
  await cl.Message(content="👋 I’m a Python Expert Assistant. Ask me anything about Python programming!").send()


# 🔹 ============== On Message Event============== 
@cl.on_message
async def main(message: cl.Message):
    try:
        result = await Runner.run(
            agent_one,
            input=message.content
        )
        await cl.Message(content=result.final_output).send()

    except InputGuardrailTripwireTriggered:
        await cl.Message(content="⚠️ Sorry, Please ask only Python programming questions.").send()
        
    except OutputGuardrailTripwireTriggered:
        await cl.Message(content="⚠️ Output blocked:").send()


# ok
# uv run chainlit run class6_output_gurdrails__input_gurdrails.py -w