import streamlit as st
from streamlit_chat import message
import openai
import os
import json
import yaml
from dotenv import load_dotenv

from metar_fetcher import fetch_metar
from taf_fetcher import get_taf
from metar_interpreter import interpret_metar
from taf_interpreter import interpret_taf
from web_search import search_web

# 🌍 Load environment
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📜 Load prompt
with open("app/prompt.yaml", "r") as f:
    prompt_data = yaml.safe_load(f)

# 🛫 Streamlit config
st.set_page_config(page_title="Aviation Weather & Flight Co-Pilot", page_icon="🛩️")
st.title("🧠 Aviation Weather & Flight Co-Pilot")
st.markdown(
    "I'm your assistant for **weather**, **regulations**, and **flight planning**.\n\n"
    "Ask for METARs, TAFs, regulation lookups, VFR decisions, or route briefings."
)

# 💬 Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": prompt_data["system"]},
        {
            "role": "assistant",
            "content": "👋 Hello, pilot. I'm your AI Co-Pilot. Ready to help with weather, planning, or FAA questions. Just type your question below to begin."
        }
    ]

# 🔧 Available tools
functions = [
    {
        "type": "function",
        "function": {
            "name": "fetch_metar",
            "description": "Get the latest METAR for a given ICAO airport code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {"type": "string", "description": "The ICAO code (e.g. KSEA)"}
                },
                "required": ["icao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_taf",
            "description": "Get the latest TAF forecast for a given ICAO airport code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icao": {"type": "string", "description": "The ICAO code (e.g. KSFO)"}
                },
                "required": ["icao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "interpret_metar",
            "description": "Interpret a raw METAR weather report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metar": {"type": "string", "description": "Raw METAR string"}
                },
                "required": ["metar"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "interpret_taf",
            "description": "Interpret a raw TAF forecast.",
            "parameters": {
                "type": "object",
                "properties": {
                    "taf": {"type": "string", "description": "Raw TAF string"}
                },
                "required": ["taf"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for recent aviation updates, news, or regulations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    }
]

# 💬 Show chat
for i, msg in enumerate(st.session_state.messages):
    if isinstance(msg, dict):
        role = msg.get("role")
        content = msg.get("content")
    else:
        role = getattr(msg, "role", None)
        content = getattr(msg, "content", None)

    if role in ("user", "assistant", "tool") and content:
        message(content, is_user=(role == "user"), key=f"msg-{i}")

# ✏️ User input
user_input = st.chat_input("Type a flight planning or aviation question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user-{len(st.session_state.messages)}")

    with st.spinner("🧠 Analyzing..."):
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
                "content": reply.content or "",
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
                elif func_name == "search_web":
                    result = search_web(**args)
                else:
                    result = f"❌ Unknown tool: {func_name}"

                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            followup = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=st.session_state.messages
            )
            reply = followup.choices[0].message

        st.session_state.messages.append(reply)
        message(reply.content, is_user=False, key=f"msg-{len(st.session_state.messages)}")
