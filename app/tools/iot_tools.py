"""
IoT Tools Module for OpenAI Realtime API
Contains smart home control functions and their tool definitions.
"""

import requests


def switch_light():
    """Toggles the smart bulb on or off via IoT API."""
    try:
        res = requests.get("https://aa63d9293a05.ngrok-free.app/switch")
        return f"Light toggled. Server says: {res.text}"
    except Exception as e:
        return f"Error toggling light: {str(e)}"


# Tool definitions for OpenAI Realtime API - FIXED FORMAT
tools = [
    {
        "type": "function",
        "name": "switch_light",
        "description": "Toggle the smart bulb on/off via IoT API.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


# Function mapping for easy execution
FUNCTION_MAP = {
    "switch_light": switch_light
}


def execute_function(function_name: str, **kwargs):
    """
    Execute a function by name with given arguments.
    
    Args:
        function_name (str): Name of the function to execute
        **kwargs: Arguments to pass to the function
        
    Returns:
        The result of the function execution
    """
    if function_name in FUNCTION_MAP:
        return FUNCTION_MAP[function_name](**kwargs)
    else:
        return f"Function '{function_name}' not found"