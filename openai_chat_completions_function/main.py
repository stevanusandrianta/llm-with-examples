from pydantic import BaseModel
from openai import OpenAI
import requests
import json

client = OpenAI()

#Structured Output
class OpenAIResponse(BaseModel):
    message: str

#Tools definition
tools = [{
    "type": "function",
    "function": {
        "name": "get_pokemon_detail",
        "description": "Get detail of a certain pokemon",
        "parameters": {
            "type": "object",
            "properties": {
                "pokemon_name": {"type": "string"},
            },
            "required": ["pokemon_name"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

SYSTEM_PROMPT = """
You are pokemon master! Your task is to tell what is the element of the pokemon that the user ask
If you don't know about it, just made something up!
"""

#Conversation State
conversation_state = [
    {"role": "system", "content": SYSTEM_PROMPT} #This will be your system prompt
]

print("Hey there! I'm a pokemon master, what pokemon you want to learn about?")
while True:
    user_input = input("You: ")
    conversation_state.append(
        {"role": "user", "content": user_input}
    )

    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=conversation_state,
        response_format=OpenAIResponse,
        tools=tools
    )

    #check whether there is a tool calls
    tool_calls = completion.choices[0].message.tool_calls
    if tool_calls == None or len(tool_calls) == 0:
        message = completion.choices[0].message.parsed.message
        print("Bot: {}".format(message))
        
        conversation_state.append(
            {"role": "assistant", "content": message}
        )
    else:
        #Records list of the functions call you need to run
        conversation_state.append(completion.choices[0].message)
        
        #Iterate for all the tools calls
        for tool_call in tool_calls:
            if tool_call.function.name == "get_pokemon_detail":
                args = json.loads(tool_call.function.arguments)
                pokemon_name = args["pokemon_name"]
                response = requests.get("http://localhost:8080/pokemon/{}".format(pokemon_name))

                print("Triggering function call with name -> {}".format(tool_call.function.name))
                print("Triggering function call with args -> {}".format(args))
                print("Triggering function call with response -> {}".format(response.json()))
            
            conversation_state.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": str(response.json())}
            )

        #Call chat completions API again once you finish the tool calls
        completion = client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=conversation_state,
            response_format=OpenAIResponse,
            tools=tools
        )
        message = completion.choices[0].message.parsed.message
        print("Bot: {}".format(message))

        conversation_state.append(
            {"role": "assistant", "content": message}
        )