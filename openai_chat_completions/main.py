from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

#Structured Output
class OpenAIResponse(BaseModel):
    message: str

SYSTEM_PROMPT = "You are dad jokes specialist. You task is to make a dad jokes based on the topic from the user"

#Conversation State
conversation_state = [
    {"role": "system", "content": SYSTEM_PROMPT} #This will be your system prompt
]

print("Hi! I'm a dad jokes specialist, what topic of jokes you want to hear today?")
while True:
    user_input = input("You: ")
    conversation_state.append(
        {"role": "user", "content": user_input}
    )

    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=conversation_state,
        response_format=OpenAIResponse,
    )

    message = completion.choices[0].message.parsed.message
    print("Bot: {}".format(message))
    
    conversation_state.append(
        {"role": "assistant", "content": message}
    )