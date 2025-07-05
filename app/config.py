"""
Configuration settings for the Aviation Weather Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AVWX_API_KEY = os.getenv("AVWX_API_KEY")

# Model Configuration
DEFAULT_MODEL = "gpt-4o-mini"
FALLBACK_MODEL = "gpt-3.5-turbo-1106"

# Request Timeouts (seconds)
METAR_TIMEOUT = 10
TAF_TIMEOUT = 10
NOTAM_TIMEOUT = 15
WEB_SEARCH_TIMEOUT = 10

# User Agent
USER_AGENT = "AviationWeatherAgent/1.0"

# NOTAM Configuration
MAX_NOTAMS_DISPLAY = 5

# TAF Configuration
NEARBY_AIRPORT_RADIUS = 10  # Number of nearby airports to check

# Validation
ICAO_PATTERN = r'^[A-Z]{4}$'

# Error Messages
ERROR_MESSAGES = {
    "missing_openai_key": "❌ OpenAI API key not set. Please check your environment variables.",
    "missing_avwx_key": "❌ AVWX API key not set. Please check your environment variables.",
    "invalid_icao": "❌ Invalid ICAO format. Must be 4 letters (e.g., KSEA, KSFO).",
    "timeout": "❌ Request timeout. Please try again.",
    "network_error": "❌ Network error. Please check your internet connection.",
    "auth_error": "❌ Authentication failed. Please check your API keys.",
    "not_found": "⚠️ Data not found. Please verify the airport code.",
    "unknown_error": "❌ Unexpected error occurred."
}

def validate_api_keys():
    """Validate that required API keys are set"""
    missing_keys = []
    
    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")
    if not AVWX_API_KEY:
        missing_keys.append("AVWX_API_KEY")
    
    return missing_keys 