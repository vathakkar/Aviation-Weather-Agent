# app/notam_fetcher.py

import requests
import re
from bs4 import BeautifulSoup

def get_notams(icao: str) -> str:
    # Validate ICAO code
    if not icao or not isinstance(icao, str):
        return "❌ Invalid ICAO code provided."
    
    # Clean and validate ICAO format (4 letters, uppercase)
    icao = icao.strip().upper()
    if not re.match(r'^[A-Z]{4}$', icao):
        return f"❌ Invalid ICAO format: {icao}. Must be 4 letters (e.g., KSEA, KSFO)."
    
    url = (
        "https://pilotweb.nas.faa.gov/PilotWeb/notamsRetrievalByICAOAction.do"
        f"?method=displayByICAOs&reportType=RAW&formatType=DOMESTIC&retrieveLocId={icao}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Try <pre> tag first
        pre = soup.find("pre")
        if not pre:
            return f"⚠️ Could not find NOTAM block for {icao}."

        raw_text = pre.get_text().strip()

        if "NO NOTAM" in raw_text.upper():
            return f"✅ No NOTAMs found for {icao}."

        # Split NOTAMs by double newline
        notams = [n.strip() for n in raw_text.split("\n\n") if n.strip()]
        if not notams:
            return f"✅ No NOTAMs found for {icao}."

        return f"📢 NOTAMs for {icao}:\n\n" + "\n\n".join(notams[:5])  # Limit to 5

    except requests.exceptions.Timeout:
        return f"❌ Timeout fetching NOTAMs for {icao}. Please try again."
    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP error fetching NOTAMs for {icao}: {http_err}"
    except requests.exceptions.RequestException as e:
        return f"❌ Network error fetching NOTAMs for {icao}: {e}"
    except Exception as e:
        return f"❌ Unexpected error fetching NOTAMs for {icao}: {e}"
