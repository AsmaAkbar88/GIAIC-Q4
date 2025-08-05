#  ye simple chainlit ka code hy 

from dotenv import load_dotenv 
from agents import ( Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
,input_guardrail , GuardrailFunctionOutput , InputGuardrailTripwireTriggered)
import os 
from pydantic import BaseModel
import asyncio

  

load_dotenv()
set_tracing_disabled (True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)


# -------------------- Input types --------------------

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


# -------------------- Input guardrail --------------------

input_guardrail_agent = Agent(
    name="Input Guardrail Check",
    instructions="Check if the user is asking you to do their math homework.",
    model=model,
    output_type=MathHomeworkOutput,
)

@input_guardrail
async def math_guardrail(ctx, agent, input):
    print("Guardrail is checking input:", input)
    result = await Runner.run(
        starting_agent=input_guardrail_agent, 
        input= input
    )

    return GuardrailFunctionOutput(
    output_info=result.final_output,
    tripwire_triggered=result.final_output.is_math_homework, 
)

# -------------------- Main agent -------------------
 #Agents:
customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent and your task is to resolve user only math queries",
    model=model,
    input_guardrails=[math_guardrail],

)
async def main():
    try:
        result = await Runner.run(
            starting_agent=customer_support_agent,
            input="what is computer?? " \
            ":"
            # input="Define newton's third law of motion?"
        )

        print("final jwb" , result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("\nMath/Input Guradrail Tripwire Triggered: ")
        reasoning = e.guardrail_result.output.output_info.reasoning
        print("reasoning  :" ,reasoning)
        print("Guardrail Result:  " , e.guardrail_result.output) # GuardrailFunctionOutput: the object return from 'math_guardrail'


if __name__ == "__main__":
    asyncio.run(main())

# output 
    # Guardrail is checking input: what is computer?? :
# final jwb I can help you with math problems. What math question do you have? 