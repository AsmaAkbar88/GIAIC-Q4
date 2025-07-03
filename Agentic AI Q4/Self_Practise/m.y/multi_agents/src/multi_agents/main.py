from dotenv import load_dotenv
from agents import Agent , Runner , OpenAIChatCompletionsModel , AsyncOpenAI , set_tracing_disabled
import os


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


#1st Agents (Web Developer Expert):
Agent1 = Agent( 
    name="Web Developer Expert", 
    instructions="Build responsive and performant websites using modern frameworks.", 
    model=model ,
    handoff_description="handoff to web developer if the task is related to web development."
)


#2nd Agents (Mobile App Developer Expert):
Agent2 = Agent( 
    name="Mobile App Developer Expert", 
    instructions="Develop cross-platform mobile apps for iOS and Android. Only english & Urdu language",
    model=model ,
    handoff_description="handoff to mobile app developer if the task is related to mobile apps."
)


#3rd Agents (Marketing Expert Agent):
Agent3 = Agent( 
    name="Marketing Expert Agent",
    instructions="Create and execute marketing strategies for product launches. Only english & Urdu language",
    model=model ,
    handoff_description="handoff to marketing agent if the task is related to marketing."
)


#manager (handoff):
async def agent(user_input):
    manager = Agent(
        name="Manager",
        instructions= "You will chat with the user and delegate tasks to specialized agents based on their requests.",
        model= model,
        handoffs=[Agent1 , Agent2 , Agent3],
        
        )


    response = await Runner.run(
        manager , 
        input = user_input
    )    
    return response.final_output