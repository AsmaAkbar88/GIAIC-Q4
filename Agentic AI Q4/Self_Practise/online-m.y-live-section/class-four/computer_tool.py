# Browser use
# Computer_Tool alternate
#uv add browser_use
# uv add langchain-google-genai
# pip install browser-use
# playwright install chromium --with-deps --no-shell
# uv pip install --upgrade langchain-google-genai
# uv pip install --upgrade browser-use


from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()
import os


async def main():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    agent = Agent(
        task="Search YouTube for   videos  on the  OpenAI Agents SDK, and recommend the best one based on relevance, views, and quality. Provide the video’s title, channel, URL, and a 100-word summary of its content, highlighting key points and why it’s the best don not play any video.",
        llm=llm,
    )
    await agent.run()
asyncio.run(main())