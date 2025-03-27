import streamlit as st
from streamlit_chat import message
import openai
import os
from dotenv import load_dotenv
import json

from metar_fetcher import fetch_metar
from taf_fetcher import get_taf
from metar_interpreter import interpret_metar
from taf_interpreter import interpret_taf
from full_brief import get_full_brief

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI setup
st.set_page_config(page_title="Aviation Weather Co-Pilot", page_icon="🛫")
st.title("🧠 Aviation Weather Co-Pilot")
st.markdown("Chat with me about aviation weather! I can fetch and interpret METARs and TAFs, and give you full weather briefings.")

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful aviation weather assistant. You can fetch and interpret METARs, TAFs, and give full flight briefings."
        },
        {
            "role": "assistant",
            "content": "👋 Hi! I'm your Aviation Weather Co-Pilot. Ask me for METARs, TAFs, or full briefings. Try something like:\n\n• What's the weather at KSFO?\n• Interpret this METAR: ...\n• Give me a full brief for KSEA"
        }
    ]

# Tools for GPT-4 Function Calling
functions = [
    {
        "type": "function",
        "function": {
            "name": "fetch_metar",
            "description": "Fetch the latest METAR report from an ICAO airport code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {
                        "type": "string",
                        "description": "The ICAO code (e.g. KSEA)"
                    }
                },
                "required": ["icao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_taf",
            "description": "Fetch the latest TAF forecast from an ICAO airport code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {
                        "type": "string",
                        "description": "The ICAO code (e.g. KSFO)"
                    }
                },
                "required": ["icao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "interpret_metar",
            "description": "Interpret a raw METAR weather report in plain English.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metar": {
                        "type": "string",
                        "description": "Raw METAR string"
                    }
                },
                "required": ["metar"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "interpret_taf",
            "description": "Interpret a raw TAF forecast in plain English.",
            "parameters": {
                "type": "object",
                "properties": {
                    "taf": {
                        "type": "string",
                        "description": "Raw TAF string"
                    }
                },
                "required": ["taf"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_full_brief",
            "description": "Generate a full weather briefing (METAR + TAF + interpretation) for an airport.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {
                        "type": "string",
                        "description": "The ICAO code (e.g. KLAX)"
                    }
                },
                "required": ["icao"]
            }
        }
    }
]

# Show chat history
for i, msg in enumerate(st.session_state.messages):
    # Only render messages that have a 'content' key
    if "content" in msg:
        message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg-{i}")


# Handle user input
user_input = st.chat_input("Type your aviation weather question here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user-{len(st.session_state.messages)}")

    with st.spinner("🛫 Getting the latest data..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=st.session_state.messages,
            tools=functions,
            tool_choice="auto"
        )

        reply = response.choices[0].message

        if reply.tool_calls:
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply.content,
                "tool_calls": [tc.model_dump() for tc in reply.tool_calls]
            })

            for tool_call in reply.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func_name == "fetch_metar":
                    result = fetch_metar(**args)
                elif func_name == "get_taf":
                    result = get_taf(**args)
                elif func_name == "interpret_metar":
                    result = interpret_metar(**args)
                elif func_name == "interpret_taf":
                    result = interpret_taf(**args)
                elif func_name == "get_full_brief":
                    result = get_full_brief(**args)
                else:
                    result = f"❌ Unknown tool: {func_name}"

                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Final GPT response after tool output
            followup = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=st.session_state.messages
            )
            reply = followup.choices[0].message

        st.session_state.messages.append(reply)
        message(reply.content, is_user=False, key=f"final-{len(st.session_state.messages)}")
