from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
from twilio.rest import Client

# 🔹 Step 1: Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

# 🔹 Step 2: Gemini LLM setup
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model=MODEL_NAME
)

# 🔹 Step 3: Tool for sending WhatsApp messages
@function_tool
def send_whatsapp_message(to: str, message: str) -> str:
    """
    Send WhatsApp message using Twilio.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_whatsapp_number = f"whatsapp:{to}"

    client = Client(account_sid, auth_token)
    msg = client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

    return f"📩 Message sent to {to}"

# 🔹 Step 4: Define Auntie agent
auntie_agent = Agent(
    name="Auntie",
    instructions="""
        You are a rishtay wali Auntie 👵.
        When user says 'Send message to <number> saying: <message>',
        use the send_whatsapp_message tool to deliver it.
    """,
    model=model,
    tools=[send_whatsapp_message]
)

# 🔹 Step 5: Loop to take input again and again
while True:
    msg = input("📨 Aap kya message bhejna chahti hain? (exit likh kar roko): ")

    if msg.lower() == "exit":
        print("👋 Chat Ended.")
        break

    # ✅ Format LLM input so it triggers the tool
    user_input = f"Send message to +923250801811 saying: {msg}"

    # ✅ Run the agent
    result = Runner.run_sync(
        starting_agent=auntie_agent,
        input=user_input
    )

    print("✅ WhatsApp Message Sent:", result.final_output)
