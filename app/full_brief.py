# app/full_brief.py

from app.metar_fetcher import fetch_metar
from app.taf_fetcher import get_taf
from app.taf_interpreter import interpret_taf

def get_full_brief(icao: str) -> str:
    icao = icao.upper()

    # Fetch METAR
    metar = fetch_metar(icao)
    if "❌" in metar:
        return f"❌ Failed to get METAR for {icao}. Skipping briefing."

    # Fetch TAF
    taf = get_taf(icao)
    if "❌" in taf:
        return f"❌ Failed to get TAF for {icao}. Skipping briefing."

    # Interpret TAF
    taf_summary_prompt = interpret_taf(taf)

    return (
        f"📋 Full Weather Briefing for `{icao}`:\n\n"
        f"---\n\n"
        f"🛰️ **METAR:**\n{metar}\n\n"
        f"---\n\n"
        f"📄 **TAF (Forecast):**\n{taf}\n\n"
        f"---\n\n"
        f"🧠 **Interpreted Forecast:**\n{taf_summary_prompt}"
    )
