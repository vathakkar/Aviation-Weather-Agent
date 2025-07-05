import os
import requests
import re

def fetch_metar(icao):
    # Validate ICAO code
    if not icao or not isinstance(icao, str):
        return "❌ Invalid ICAO code provided."
    
    # Clean and validate ICAO format (4 letters, uppercase)
    icao = icao.strip().upper()
    if not re.match(r'^[A-Z]{4}$', icao):
        return f"❌ Invalid ICAO format: {icao}. Must be 4 letters (e.g., KSEA, KSFO)."
    
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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        raw_metar = data.get("raw")
        
        if not raw_metar:
            return f"⚠️ No METAR data available for {icao}."
            
        return raw_metar
        
    except requests.exceptions.Timeout:
        return f"❌ Timeout fetching METAR for {icao}. Please try again."
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"⚠️ METAR not found for {icao}. Please verify the airport code."
        elif response.status_code == 401:
            return f"❌ Authentication failed. Please check your AVWX API key."
        else:
            return f"❌ HTTP error {response.status_code} for {icao}: {http_err}"
    except requests.exceptions.RequestException as e:
        return f"❌ Network error fetching METAR for {icao}: {e}"
    except Exception as e:
        return f"❌ Unexpected error fetching METAR for {icao}: {e}"
