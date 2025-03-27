# app/interpret_metar.py

def interpret_metar(metar: str) -> str:
    if not metar.strip():
        return "❌ No METAR provided for interpretation."

    return (
        f"📝 Please interpret the following METAR in plain English:\n\n"
        f"{metar}\n\n"
        "Break down the wind, visibility, temperature, altimeter setting, cloud layers, and any special weather remarks. "
        "Mention if conditions are VFR, MVFR, or IFR."
    )
