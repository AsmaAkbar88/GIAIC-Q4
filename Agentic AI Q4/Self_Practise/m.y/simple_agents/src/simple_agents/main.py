from dotenv import load_dotenv
from agents import Agent , Runner , OpenAIChatCompletionsModel , AsyncOpenAI , set_tracing_disabled
import os

async def agent(user_input):
    load_dotenv()
    set_tracing_disabled(True)

    provider = AsyncOpenAI( 
       api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
    )
    model = OpenAIChatCompletionsModel( 
        model="gemini-2.0-flash-exp", 
        openai_client=provider, 
    )
    Agent1 = Agent( 
        name="Assistant", 
        instructions="ye sab sy sirf bat kry ga un ko agr koi saad hy tu osy happy kry ga or joke suniye ga.", 
        model=model 
    )

    response = Runner.run_sync(
        starting_agent= Agent1,
        input= user_input
    )    

    return response.final_output