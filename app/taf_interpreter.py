# app/taf_interpreter.py

def interpret_taf(taf: str) -> str:
    if not taf.strip():
        return "❌ No TAF provided for interpretation."
    
    return f"📄 Here's a plain-English summary of the TAF:\n\n\"{taf}\"\n\nPlease explain the periods, wind changes, visibility, precipitation, and cloud layers in detail."
