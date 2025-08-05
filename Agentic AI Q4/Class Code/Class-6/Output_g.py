import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,output_guardrail , set_tracing_disabled ,
    GuardrailFunctionOutput, OutputGuardrailTripwireTriggered )
from pydantic import BaseModel


load_dotenv()
set_tracing_disabled (True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

# -------------------- Output types --------------------

class PhysicsHomeworkOutput(BaseModel):
    is_physics_homework: bool
    reasoning: str

class MainMessageOutput(BaseModel):
    response: str


# -------------------- Output guardrail --------------------
output_guardrail_agent = Agent(
    name="Ouput Guardrail Check",
    instructions="Check if the user is asking you to do their physics homework.",
    model=model,
    output_type=PhysicsHomeworkOutput,
)

@output_guardrail
async def physics_guardrail(ctx, agent, output):
    print("\nOutput Guardrail Prompt: \n", output)
    result = await Runner.run(starting_agent=output_guardrail_agent, input=output.response)
    

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_physics_homework,
    )

    

# -------------------- Main agent -------------------
 #Agents:
customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent and your task is to resolve user queries",
    model=model,
    output_guardrails=[physics_guardrail],
    output_type=MainMessageOutput,
)


async def main():
    try:
        result = await Runner.run(
            starting_agent=customer_support_agent,
            # input="Give me the answer of 2 + 2:"
            input="Define newton's third law of motion?"
        )

        # print(result.final_output)
    
    except OutputGuardrailTripwireTriggered as e:
        print("\nPhysics/Output Guradrail Tripwire Triggered: \n ")
        reasoning = e.guardrail_result.output.output_info.reasoning
        print("Reasoing :" , reasoning)
        print("Guardrail:  " , e.guardrail_result.output) # GuardrailFunctionOutput: the object return from 'physics_guardrail'



if __name__ == "__main__":
    asyncio.run(main())