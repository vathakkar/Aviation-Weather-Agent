# app/metar_interpreter.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def interpret_metar(metar_text):
    prompt = f"""
You are an aviation weather assistant. Analyze the following METAR and help the user make a go/no-go flight decision.

METAR: {metar_text}

1. Decode the METAR into plain English.
2. State whether it's VFR, MVFR, IFR, or LIFR according to FAA rules.
3. Explain the wind conditions (direction, speed, gusts).
4. Ask the user about their personal minimums and advise if this is safe to fly.
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
