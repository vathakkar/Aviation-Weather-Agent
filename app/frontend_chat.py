import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
import openai
import json

from metar_fetcher import fetch_metar
from metar_interpreter import interpret_metar

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

st.set_page_config(page_title="Aviation Weather Agent", page_icon="🛫")
st.title("🛫 Aviation Weather Agent")

# Define GPT tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_metar",
            "description": "Fetch the raw METAR report from an ICAO airport code",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {
                        "type": "string",
                        "description": "4-letter ICAO airport code (e.g., KSEA)"
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
            "description": "Interpret the raw METAR into plain English",
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
    }
]

# ✅ Initialize chat memory and welcome message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an aviation weather assistant that uses tools to fetch and explain METAR reports."},
        {"role": "assistant", "content": "👋 Hi there! I’m your Aviation Weather Assistant.\n\nYou can ask me things like:\n• 'What’s the weather at KSEA?'\n• 'Show me the METAR for KLAX'\n• 'Can I fly from JFK right now?'\n\nJust enter an ICAO code or ask a question to get started!"}
    ]

# Show chat history
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] != "system":
        message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg-{i}")

# Get user input
user_input = st.chat_input("Ask about airport weather or METAR...")

if user_input:
    # ✅ Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user-msg-{len(st.session_state.messages)}")

    # ⏳ Show spinner while GPT processes
    with st.spinner("🤖 Thinking..."):

        # GPT initial response (might include tool call)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto"
        )

        reply = response.choices[0].message

        if reply.tool_calls:
            # ✅ Save assistant message with tool calls
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply.content,
                "tool_calls": [tc.model_dump() for tc in reply.tool_calls]
            })

            for tool_call in reply.tool_calls:
                func_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                tool_call_id = tool_call.id

                if func_name == "fetch_metar":
                    result = fetch_metar(arguments["icao"])
                elif func_name == "interpret_metar":
                    result = interpret_metar(arguments["metar"])
                else:
                    result = f"⚠️ Unknown tool: {func_name}"

                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result
                })

            # GPT continues with tool output
            followup = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=st.session_state.messages
            )

            final_reply = followup.choices[0].message
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_reply.content
            })
            message(final_reply.content, key=f"final-{len(st.session_state.messages)}")

        else:
            # No tool used, just assistant reply
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply.content
            })
            message(reply.content, key=f"final-{len(st.session_state.messages)}")
