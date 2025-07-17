from agents import Agent, Runner, function_tool , OpenAIChatCompletionsModel , AsyncOpenAI
from dotenv import load_dotenv
import os
from twilio.rest import Client  # Twilio Python SDK


load_dotenv()  # This will load the .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
MODEL_NAME = "gemini-2.0-flash"

if not GEMINI_API_KEY:
    raise ValueError("KEY NOT FOUND")

external_client = AsyncOpenAI(
 api_key = GEMINI_API_KEY ,
 base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client= external_client ,
    model= MODEL_NAME 
)

@function_tool
def send_whatsapp_message(to: str, message: str) -> str:
    """
    Send WhatsApp message to a given number using Twilio
    Example input: to="+923250801811", message="Hello from Auntie!"
    """
    # Environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_whatsapp_number = f"whatsapp:{to}"

    # Twilio client
    client = Client(account_sid, auth_token)

    # Send message
    msg = client.messages.create(
        body= message,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

    return f"Message sent to {+923250801811}"

# Agent with tool
auntie = Agent(
    name="Auntie",
    instructions="You're a rishtay wali Auntie who can send WhatsApp messages.",
    tools=[send_whatsapp_message],
    model=model
)

# Agent input
result = Runner.run_sync(
    starting_agent=auntie,
    input="Send a message to +923250801811 saying: agr koi doctr ka risth ahy tu btna mjy ."
)

print(result.final_output)
