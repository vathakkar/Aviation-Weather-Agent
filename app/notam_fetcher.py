# app/notam_fetcher.py

import requests
from bs4 import BeautifulSoup

def get_notams(icao: str) -> str:
    icao = icao.upper()
    url = (
        "https://pilotweb.nas.faa.gov/PilotWeb/notamsRetrievalByICAOAction.do"
        f"?method=displayByICAOs&reportType=RAW&formatType=DOMESTIC&retrieveLocId={icao}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Try <pre> tag first
        pre = soup.find("pre")
        if not pre:
            return f"⚠️ Could not find NOTAM block for `{icao}`."

        raw_text = pre.get_text().strip()

        if "NO NOTAM" in raw_text.upper():
            return f"✅ No NOTAMs found for `{icao}`."

        # Split NOTAMs by double newline
        notams = [n.strip() for n in raw_text.split("\n\n") if n.strip()]
        if not notams:
            return f"✅ No NOTAMs found for `{icao}`."

        return f"📢 NOTAMs for {icao}:\n\n" + "\n\n".join(notams[:5])  # Limit to 5

    except Exception as e:
        return f"❌ Error fetching NOTAMs for `{icao}`: {e}"
