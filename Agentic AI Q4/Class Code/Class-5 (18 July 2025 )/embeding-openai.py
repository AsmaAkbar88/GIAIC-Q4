# Embedding - File Search Tool
# How to create a Vector Database
# Go to Open AI Platform -> Dashboard -> storage -> vector stores ->
# create db -> add files -> upload your file -> attach -> copy vector store id and save
# ________________________________________________________________________________________
# cell 01
# !pip install -qU openai-agents

# cell 02
# import nest_asyncio
# nest_asyncio.apply()  # To run async functions in google colab notebook

# cell 03
# import os
# from google.colab import userdata

# API_KEY = userdata.get("OPENAI_API_KEY")  # Get api key from google secrets
# os.environ["OPENAI_API_KEY"] = API_KEY    # To set api key in environment variables


# cell 04
import asyncio
from agents import Agent, Runner, FileSearchTool


agent = Agent(
    name="Assistant",
    instructions="""
        You are acting as me, the owner of this service.
        Always speak in the first person, as if you are the person providing the service.
        Be friendly, concise, and helpful. Clearly explain what I offer, answer questions,
        and keep the conversation natural and tailored to the user's needs.
        Ask clarifying questions if needed to better assist them.
    """,
    tools=[
        FileSearchTool( #! FileSearchTool will only work with OpenAI API key,
            max_num_results=3,
            vector_store_ids=["YOUR_VECTOR_STORE_ID"],
        )
    ]
)

async def main():
    result = await Runner.run(agent, input="what is your name")
    print(result.final_output)


asyncio.run(main())
