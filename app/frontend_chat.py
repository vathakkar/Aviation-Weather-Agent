# app/frontend_chat.py

import streamlit as st
from streamlit_chat import message
from metar_fetcher import fetch_metar
from metar_interpreter import interpret_metar

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Aviation Weather Co-Pilot", page_icon="🛫")

st.title("🧠 Aviation Weather Co-Pilot")
st.markdown("Chat with me about aviation weather conditions. I can interpret METARs and help you decide if it's a good day to fly.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hi! I'm your aviation co-pilot. Give me an ICAO code like `KSEA` and I’ll fetch the METAR and interpret it for you."}
    ]

def process_input(user_input):
    if len(user_input.strip()) == 4 and user_input.isalpha():
        icao = user_input.upper()
        metar = fetch_metar(icao)
        print(f"[DEBUG] METAR result: {metar}")
        if "Error" in metar or "⚠️" in metar or "❌" in metar:
            return f"❌ Couldn't fetch METAR for `{icao}`. Please check the ICAO code."
        interpretation = interpret_metar(metar)
        return interpretation
    else:
        return "✈️ Please provide a valid 4-letter ICAO airport code (like KJFK or EGLL)."


# Display chat messages
# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg-{i}")


# User input
user_input = st.chat_input("Type an ICAO code (e.g., KSFO)...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    ai_response = process_input(user_input)
    st.session_state.messages.append({"role": "ai", "content": ai_response})
    st.rerun()

