import os
import requests

def fetch_metar(icao):
    api_key = os.getenv("AVWX_API_KEY")
    if not api_key:
        return "❌ AVWX API key not set. Please check your environment variables."

    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
        "User-Agent": "AviationWeatherAgent/1.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data.get("raw", f"⚠️ METAR not found for `{icao}`.")
    except requests.exceptions.HTTPError as http_err:
        return f"❌ AVWX HTTP error for `{icao}`: {http_err}"
    except Exception as e:
        return f"❌ Failed to fetch METAR for `{icao}` from AVWX: {e}"
