import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

async def main():

    urdu_translator = Agent(
        name="Urdu Translator",
        instructions="You are a helpful translator that translates text to Urdu.",
        model=model,
    )
    
    arabic_translator = Agent(
        name="Arabic Translator",
        instructions="You are a helpful translator that translates text to Arabic.",
        model=model,
    )
    
    french_translator = Agent(
        name="French Translator",
        instructions="You are a helpful translator that translates text to French.",
        model=model,
    )


    main_agent = Agent(
        name="Main Agent",
        instructions="""
        You have to take the user's input and call the appropriate handoff to translate the user's input.
        If you don't find appropriate handoff than simply refuse the user.
        """,
        model=model,
        handoffs=[urdu_translator, arabic_translator, french_translator]
    )

    
    result = await Runner.run(
        starting_agent=main_agent,
        input="Translate how are you in arabic"
    )
    print(result.final_output)




if __name__ == "__main__":
    asyncio.run(main())
