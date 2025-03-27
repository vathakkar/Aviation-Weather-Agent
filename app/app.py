# app/app.py
import traceback
import os
import openai
from dotenv import load_dotenv
from app.metar_fetcher import fetch_metar
from app.metar_interpreter import interpret_metar

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Tool 1: Fetch METAR by ICAO
def fetch_metar_tool(args):
    icao = args.get("icao")
    return fetch_metar(icao)

# Tool 2: Interpret METAR
def interpret_metar_tool(args):
    metar_text = args.get("metar_text")
    return interpret_metar(metar_text)

# Define tool schema for GPT function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_metar_tool",
            "description": "Fetches the latest METAR for an ICAO code",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {
                        "type": "string",
                        "description": "The 4-letter ICAO code for an airport, e.g., KSFO or KSEA"
                    }
                },
                "required": ["icao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "interpret_metar_tool",
            "description": "Interprets a raw METAR string into plain English and VFR/IFR guidance",
            "parameters": {
                "type": "object",
                "properties": {
                    "metar_text": {
                        "type": "string",
                        "description": "Raw METAR string from a weather source"
                    }
                },
                "required": ["metar_text"]
            }
        }
    }
]

# Bind tool name to function
tool_map = {
    "fetch_metar_tool": fetch_metar_tool,
    "interpret_metar_tool": interpret_metar_tool,
}

def chat():
    messages = [{"role": "system", "content": "You are an aviation weather assistant for pilots."}]
    print("🛫 Aviation Weather Agent — Ask me anything (type 'exit' to quit)")

    while True:
        user_input = input("\n🧑 You: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        reply = response.choices[0].message

        if reply.get("tool_calls"):
            for tool_call in reply.tool_calls:
                func_name = tool_call.function.name
                args = eval(tool_call.function.arguments)

                result = tool_map[func_name](args)
                messages.append({
                    "role": "function",
                    "name": func_name,
                    "content": result
                })

                # Rerun chat to integrate tool result
                second_response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=messages
                )
                final_message = second_response.choices[0].message["content"]
                print("\n🤖 AI:", final_message)
                messages.append({"role": "assistant", "content": final_message})

        else:
            print("\n🤖 AI:", reply["content"])
            messages.append({"role": "assistant", "content": reply["content"]})


if __name__ == "__main__":
    try:
        chat()
    except Exception:
        traceback.print_exc()
