# # app/taf_fetcher.py

# import os
# import requests

# def get_taf(icao: str) -> str:
#     api_key = os.getenv("AVWX_API_KEY")
#     if not api_key:
#         return "❌ AVWX API key not set in environment."

#     url = f"https://avwx.rest/api/taf/{icao}"
#     headers = {
#         "Authorization": api_key,
#         "Accept": "application/json",
#         "User-Agent": "AviationWeatherAgent/1.0"
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()

#         raw = data.get("raw", "")
#         forecast = data.get("forecast", [])
#         if not raw:
#             return f"⚠️ No TAF available for `{icao}`."

#         taf_text = f"📄 TAF for {icao}:\n{raw}\n"

#         # if forecast:
#         #     taf_text += "\n🕐 Forecast periods:\n"
#         #     for f in forecast[:3]:  # Show 3 periods max
#         #         taf_text += f"- From {f.get('start_time', {}).get('repr', '')} to {f.get('end_time', {}).get('repr', '')}: "
#         #         taf_text += f"{f.get('summary', '') or 'No summary'}\n"

#         return taf_text.strip()

#     except Exception as e:
#         return f"❌ Error fetching TAF for `{icao}`: {e}"

# app/taf_fetcher.py

import os
import requests
import re

def get_taf(icao: str) -> str:
    """
    Fetch the latest TAF for the given ICAO airport.
    If unavailable, tries to find TAFs from nearby airports.
    """
    # Validate ICAO code
    if not icao or not isinstance(icao, str):
        return "❌ Invalid ICAO code provided."
    
    # Clean and validate ICAO format (4 letters, uppercase)
    icao = icao.strip().upper()
    if not re.match(r'^[A-Z]{4}$', icao):
        return f"❌ Invalid ICAO format: {icao}. Must be 4 letters (e.g., KSEA, KSFO)."
    
    api_key = os.getenv("AVWX_API_KEY")
    if not api_key:
        return "❌ AVWX API key not set in environment."

    base_url = f"https://avwx.rest/api/taf/{icao}"
    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
        "User-Agent": "AviationWeatherAgent/1.0"
    }

    try:
        # First try for the given airport
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        raw = data.get("raw", "")
        if raw:
            return f"📄 TAF for {icao}:\n{raw}"

        # No TAF found for primary, now search vicinity
        search_url = f"https://avwx.rest/api/station/{icao}"
        station_response = requests.get(search_url, headers=headers, timeout=10)
        station_response.raise_for_status()
        station_data = station_response.json()

        latitude = station_data.get("latitude")
        longitude = station_data.get("longitude")
        if not latitude or not longitude:
            return f"⚠️ No TAF available for {icao}, and unable to find nearby airports."

        # Search nearby airports within 20NM
        nearby_url = f"https://avwx.rest/api/station?near={latitude},{longitude}&n=10"
        nearby_response = requests.get(nearby_url, headers=headers, timeout=10)
        nearby_response.raise_for_status()
        nearby_airports = nearby_response.json()

        for station in nearby_airports:
            nearby_icao = station.get("icao")
            if nearby_icao and nearby_icao != icao:
                # Try fetching TAF from nearby airport
                nearby_taf_url = f"https://avwx.rest/api/taf/{nearby_icao}"
                nearby_taf_response = requests.get(nearby_taf_url, headers=headers, timeout=10)
                nearby_taf_response.raise_for_status()
                nearby_taf_data = nearby_taf_response.json()
                nearby_raw = nearby_taf_data.get("raw", "")
                if nearby_raw:
                    return f"📄 No TAF for {icao}, but found nearby at {nearby_icao}:\n{nearby_raw}"

        return f"⚠️ No TAF available for {icao} or nearby airports."

    except requests.exceptions.Timeout:
        return f"❌ Timeout fetching TAF for {icao}. Please try again."
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"⚠️ TAF not found for {icao}. Please verify the airport code."
        elif response.status_code == 401:
            return f"❌ Authentication failed. Please check your AVWX API key."
        else:
            return f"❌ HTTP error {response.status_code} for {icao}: {http_err}"
    except requests.exceptions.RequestException as e:
        return f"❌ Network error fetching TAF for {icao}: {e}"
    except Exception as e:
        return f"❌ Unexpected error fetching TAF for {icao}: {e}"

