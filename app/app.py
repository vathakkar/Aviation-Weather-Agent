# # app/app.py
# import traceback
# import json
# import os
# import openai
# from dotenv import load_dotenv
# from app.metar_fetcher import fetch_metar
# from app.metar_interpreter import interpret_metar

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Tool 1: Fetch METAR by ICAO
# def fetch_metar_tool(args):
#     icao = args.get("icao")
#     return fetch_metar(icao)

# # Tool 2: Interpret METAR
# def interpret_metar_tool(args):
#     metar_text = args.get("metar_text")
#     return interpret_metar(metar_text)

# # Define tool schema for GPT function calling
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "fetch_metar_tool",
#             "description": "Fetches the latest METAR for an ICAO code",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "icao": {
#                         "type": "string",
#                         "description": "The 4-letter ICAO code for an airport, e.g., KSFO or KSEA"
#                     }
#                 },
#                 "required": ["icao"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "interpret_metar_tool",
#             "description": "Interprets a raw METAR string into plain English and VFR/IFR guidance",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "metar_text": {
#                         "type": "string",
#                         "description": "Raw METAR string from a weather source"
#                     }
#                 },
#                 "required": ["metar_text"]
#             }
#         }
#     }
# ]

# # Bind tool name to function
# tool_map = {
#     "fetch_metar_tool": fetch_metar_tool,
#     "interpret_metar_tool": interpret_metar_tool,
# }

# def chat():
#     messages = [
#     {
#         "role": "system",
#         "content": (
#             "You are an aviation weather assistant for pilots. "
#             "If a user asks about the weather at an airport, you should first use the `fetch_metar_tool` "
#             "to get the latest METAR for their ICAO code. Print the METAR. Then use `interpret_metar_tool` to decode and explain the METAR. "
#             "Always call the tools before answering questions related to airport weather."
#         )
#     }
# ]

#     print("🛫 Aviation Weather Agent — Ask me anything (type 'exit' to quit)")

#     while True:
#         user_input = input("\n🧑 You: ")
#         if user_input.lower() == "exit":
#             break

#         messages.append({"role": "user", "content": user_input})

#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages,
#             tools=tools,
#             tool_choice="auto"
#         )

#         reply = response.choices[0].message

#         if reply.tool_calls:
#             for tool_call in reply.tool_calls:
#                 func_name = tool_call.function.name
#                 args = eval(tool_call.function.arguments)

#                 result = tool_map[func_name](args)
#                 messages.append({
#                     "role": "function",
#                     "name": func_name,
#                     "content": result
#                 })

#                 # Rerun chat to integrate tool result
#                 second_response = openai.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=messages
#                 )
#                 final_message = second_response.choices[0].message.content
#                 print("\n🤖 AI:", final_message)
#                 messages.append({"role": "assistant", "content": final_message})

#         else:
#             print("\n🤖 AI:", reply["content"])
#             messages.append({"role": "assistant", "content": reply["content"]})


# if __name__ == "__main__":
#     try:
#         chat()
#     except Exception:
#         traceback.print_exc()


import os
import openai
from dotenv import load_dotenv
from metar_fetcher import fetch_metar
from metar_interpreter import interpret_metar

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

functions = [
    {
        "name": "fetch_metar",
        "description": "Fetch the latest METAR report from an ICAO airport code.",
        "parameters": {
            "type": "object",
            "properties": {
                "icao": {
                    "type": "string",
                    "description": "The ICAO code for the airport (e.g. KSEA, KSFO)"
                }
            },
            "required": ["icao"]
        }
    },
    {
        "name": "interpret_metar",
        "description": "Interpret a raw METAR weather report into human-friendly flight conditions.",
        "parameters": {
            "type": "object",
            "properties": {
                "metar": {
                    "type": "string",
                    "description": "The raw METAR string to interpret."
                }
            },
            "required": ["metar"]
        }
    }
]

def chat():
    messages = [
        {"role": "system", "content": "You are a helpful aviation weather assistant. You can fetch METAR reports and interpret them to tell pilots whether conditions are VFR or IFR, and what the winds and visibility are like."}
    ]

    while True:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=functions,
            tool_choice="auto"
        )

        reply = response.choices[0].message

        if reply.tool_calls:
            for tool_call in reply.tool_calls:
                func_name = tool_call.function.name
                args = tool_call.function.arguments

                if func_name == "fetch_metar":
                    from json import loads
                    args = loads(args)
                    result = fetch_metar(**args)
                elif func_name == "interpret_metar":
                    from json import loads
                    args = loads(args)
                    result = interpret_metar(**args)
                else:
                    result = f"❌ Unknown tool: {func_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                followup = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages
                )

                reply = followup.choices[0].message

        print(f"\n🤖 AI: {reply.content}")
        messages.append(reply)

if __name__ == "__main__":
    chat()
