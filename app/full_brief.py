# full_brief.py

from metar_fetcher import fetch_metar
from metar_interpreter import interpret_metar
from taf_fetcher import get_taf
from taf_interpreter import interpret_taf


def get_full_brief(icao: str) -> str:
    icao = icao.upper()

    # Fetch METAR
    metar_raw = fetch_metar(icao)
    if "❌" in metar_raw:
        return f"❌ Failed to retrieve METAR for {icao}.\n{metar_raw}"

    metar_interpretation = interpret_metar(metar_raw)

    # Fetch TAF
    taf_raw = get_taf(icao)
    if "❌" in taf_raw:
        return f"❌ Failed to retrieve TAF for {icao}.\n{taf_raw}"

    taf_interpretation = interpret_taf(taf_raw)

    # ✅ VFR Flight Summary Logic (basic heuristic)
    vfr_recommendation = "🟢 Based on current data, VFR flight looks possible in the next couple hours." \
        if all(x not in taf_raw for x in ["IFR", "LIFR", "BKN002", "OVC002", "1SM", "TSRA", "FG"]) \
        else "🔴 Conditions suggest potential IFR or marginal VFR. Caution advised."

    # ✈️ Final Output
    return (
        f"📋 Full Weather Briefing for **{icao}**\n\n"
        f"---\n\n"
        f"🛰️ **Raw METAR:**\n{metar_raw}\n\n"
        f"🧠 **Interpreted METAR:**\n{metar_interpretation}\n\n"
        f"---\n\n"
        f"📝 **Raw TAF:**\n{taf_raw}\n\n"
        f"🧠 **Interpreted TAF:**\n{taf_interpretation}\n\n"
        f"---\n\n"
        f"✈️ **Overall VFR Recommendation:**\n{vfr_recommendation}"
    )


# Optional: Run standalone for testing
if __name__ == "__main__":
    print(get_full_brief("KSEA"))
