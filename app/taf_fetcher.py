# app/taf_fetcher.py

import os
import requests

def get_taf(icao: str) -> str:
    api_key = os.getenv("AVWX_API_KEY")
    if not api_key:
        return "❌ AVWX API key not set in environment."

    url = f"https://avwx.rest/api/taf/{icao}"
    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
        "User-Agent": "AviationWeatherAgent/1.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        raw = data.get("raw", "")
        forecast = data.get("forecast", [])
        if not raw:
            return f"⚠️ No TAF available for `{icao}`."

        taf_text = f"📄 TAF for {icao}:\n{raw}\n"

        # if forecast:
        #     taf_text += "\n🕐 Forecast periods:\n"
        #     for f in forecast[:3]:  # Show 3 periods max
        #         taf_text += f"- From {f.get('start_time', {}).get('repr', '')} to {f.get('end_time', {}).get('repr', '')}: "
        #         taf_text += f"{f.get('summary', '') or 'No summary'}\n"

        return taf_text.strip()

    except Exception as e:
        return f"❌ Error fetching TAF for `{icao}`: {e}"