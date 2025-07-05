"""
Utility functions for the Aviation Weather Agent
"""
import re
import logging
from typing import Optional
from config import ICAO_PATTERN, ERROR_MESSAGES

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_icao(icao: str) -> tuple[bool, Optional[str]]:
    """
    Validate ICAO airport code format
    
    Args:
        icao: The ICAO code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not icao or not isinstance(icao, str):
        return False, ERROR_MESSAGES["invalid_icao"]
    
    # Clean and validate ICAO format (4 letters, uppercase)
    icao_clean = icao.strip().upper()
    if not re.match(ICAO_PATTERN, icao_clean):
        return False, f"❌ Invalid ICAO format: {icao}. Must be 4 letters (e.g., KSEA, KSFO)."
    
    return True, icao_clean

def format_error_response(error_type: str, context: str = "") -> str:
    """
    Format error responses consistently
    
    Args:
        error_type: Type of error from ERROR_MESSAGES
        context: Additional context (e.g., airport code)
        
    Returns:
        Formatted error message
    """
    base_message = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["unknown_error"])
    if context:
        return f"{base_message} Context: {context}"
    return base_message

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text: Raw input text
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$', '(', ')']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to prevent overly long responses
    
    Args:
        text: Text to truncate
        max_length: Maximum length allowed
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "... [truncated]"

def log_api_call(function_name: str, parameters: dict, success: bool, error: str = None):
    """
    Log API calls for debugging and monitoring
    
    Args:
        function_name: Name of the function called
        parameters: Parameters passed to the function
        success: Whether the call was successful
        error: Error message if failed
    """
    if success:
        logger.info(f"API call successful: {function_name} with params {parameters}")
    else:
        logger.error(f"API call failed: {function_name} with params {parameters}, error: {error}") 