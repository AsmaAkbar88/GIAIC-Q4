# https://github.com/syeda-hoorain-ali/giaic-q3/blob/main/class-12/guardrails.py

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled , 
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, 
    RunContextWrapper, TResponseInputItem, input_guardrail, output_guardrail
)
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

# -------------------- Output types --------------------

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


class PhysicsHomeworkOutput(BaseModel):
    is_physics_homework: bool
    reasoning: str

class MainMessageOutput(BaseModel):
    response: str


# -------------------- Input guardrail --------------------

input_guardrail_agent = Agent(
    name="Input Guardrail Check",
    instructions="Check if the user is asking you to do their math homework.",
    model=model,
    output_type=MathHomeworkOutput,
)

@input_guardrail
async def math_guardrail(ctx, agent, input):
#     ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
    print("Input Guardrail Prompt: ", input)
    result = await Runner.run(starting_agent=input_guardrail_agent, input=input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


# -------------------- Output guardrail --------------------

output_guardrail_agent = Agent(
    name="Ouput Guardrail Check",
    instructions="Check if the user is asking you to do their physics homework.",
    model=model,
    output_type=PhysicsHomeworkOutput,
)

@output_guardrail
async def physics_guardrail(ctx, agent, output):
#     ctx: RunContextWrapper[None], agent: Agent, output: MainMessageOutput
    print("Output Guardrail Prompt: ", output)
    result = await Runner.run(starting_agent=output_guardrail_agent, input=output.response)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_physics_homework,
    )


# -------------------- Main agent --------------------    

customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent and your task is to resolve user queries",
    model=model,
    input_guardrails=[math_guardrail],
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

        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("\nMath/Input Guradrail Tripwire Triggered: ")
        reasoning = e.guardrail_result.output.output_info.reasoning
        print(reasoning)
        print(e.guardrail_result.output) # GuardrailFunctionOutput: the object return from 'math_guardrail'

    except OutputGuardrailTripwireTriggered as e:
        print("\nPhysics/Output Guradrail Tripwire Triggered: ")
        reasoning = e.guardrail_result.output.output_info.reasoning
        print(reasoning)
        # print(e.guardrail_result.output) # GuardrailFunctionOutput: the object return from 'physics_guardrail'



if __name__ == "__main__":
    asyncio.run(main())