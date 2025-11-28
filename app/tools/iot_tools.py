"""
IoT Multi-Light Tools Module for OpenAI Realtime API
Contains smart home control functions for multiple colored lights and their tool definitions.
"""

import requests

BASE_URL = "http://3.110.182.220:3000"


# Individual light control functions
def turn_red_light_on():
    """Turn the red light ON via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/red/on")
        response_data = res.json()
        return response_data.get("message", "Red light turned on.")
    except Exception as e:
        return f"Error turning red light on: {str(e)}"


def turn_red_light_off():
    """Turn the red light OFF via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/red/off")
        response_data = res.json()
        return response_data.get("message", "Red light turned off.")
    except Exception as e:
        return f"Error turning red light off: {str(e)}"


def toggle_red_light():
    """Toggle the red light on/off via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/red/toggle")
        response_data = res.json()
        return response_data.get("message", "Red light toggled.")
    except Exception as e:
        return f"Error toggling red light: {str(e)}"


def turn_white_light_on():
    """Turn the blue light ON via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/blue/on")
        response_data = res.json()
        return response_data.get("message", "White light turned on.")
    except Exception as e:
        return f"Error turning blue light on: {str(e)}"


def turn_white_light_off():
    """Turn the blue light OFF via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/blue/off")
        response_data = res.json()
        return response_data.get("message", "White light turned off.")
    except Exception as e:
        return f"Error turning blue light off: {str(e)}"


def toggle_white_light():
    """Toggle the White light on/off via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/blue/toggle")
        response_data = res.json()
        return response_data.get("message", "White light toggled.")
    except Exception as e:
        return f"Error toggling blue light: {str(e)}"


def turn_green_light_on():
    """Turn the green light ON via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/green/on")
        response_data = res.json()
        return response_data.get("message", "Green light turned on.")
    except Exception as e:
        return f"Error turning green light on: {str(e)}"


def turn_green_light_off():
    """Turn the green light OFF via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/green/off")
        response_data = res.json()
        return response_data.get("message", "Green light turned off.")
    except Exception as e:
        return f"Error turning green light off: {str(e)}"


def toggle_green_light():
    """Toggle the green light on/off via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/green/toggle")
        response_data = res.json()
        return response_data.get("message", "Green light toggled.")
    except Exception as e:
        return f"Error toggling green light: {str(e)}"


def turn_yellow_light_on():
    """Turn the yellow light ON via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/yellow/on")
        response_data = res.json()
        return response_data.get("message", "Yellow light turned on.")
    except Exception as e:
        return f"Error turning yellow light on: {str(e)}"


def turn_yellow_light_off():
    """Turn the yellow light OFF via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/yellow/off")
        response_data = res.json()
        return response_data.get("message", "Yellow light turned off.")
    except Exception as e:
        return f"Error turning yellow light off: {str(e)}"


def toggle_yellow_light():
    """Toggle the yellow light on/off via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/yellow/toggle")
        response_data = res.json()
        return response_data.get("message", "Yellow light toggled.")
    except Exception as e:
        return f"Error toggling yellow light: {str(e)}"


# All lights control functions
def turn_all_lights_on():
    """Turn ALL lights ON via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/all/on")
        response_data = res.json()
        return response_data.get("message", "All lights turned on.")
    except Exception as e:
        return f"Error turning all lights on: {str(e)}"


def turn_all_lights_off():
    """Turn ALL lights OFF via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/all/off")
        response_data = res.json()
        return response_data.get("message", "All lights turned off.")
    except Exception as e:
        return f"Error turning all lights off: {str(e)}"


def toggle_all_lights():
    """Toggle ALL lights on/off via IoT API."""
    try:
        res = requests.get(f"{BASE_URL}/all/toggle")
        response_data = res.json()
        return response_data.get("message", "All lights toggled.")
    except Exception as e:
        return f"Error toggling all lights: {str(e)}"


# Status functions
def get_all_lights_status():
    """Get the current status of all lights."""
    try:
        res = requests.get(f"{BASE_URL}/status")
        response_data = res.json()
        if response_data.get("connected"):
            light_states = response_data.get("lightStates", {})
            status_messages = []
            for color, state in light_states.items():
                status_messages.append(f"{color.capitalize()} light: {state}")
            return "Light Status: " + ", ".join(status_messages)
        else:
            return "ESP32 not connected. Cannot get light status."
    except Exception as e:
        return f"Error getting lights status: {str(e)}"


def get_light_status(color):
    """Get the status of a specific colored light."""
    try:
        res = requests.get(f"{BASE_URL}/status/{color.lower()}")
        response_data = res.json()
        return response_data.get(
            "message", f"{color.capitalize()} light status unknown."
        )
    except Exception as e:
        return f"Error getting {color} light status: {str(e)}"


# Tool definitions for OpenAI Realtime API
tools = [
    # Individual Red Light Controls
    {
        "type": "function",
        "name": "turn_red_light_on",
        "description": "Turn the red light ON. Use when user asks to turn on red light, red lamp, or mentions red color lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "turn_red_light_off",
        "description": "Turn the red light OFF. Use when user asks to turn off red light, red lamp, or disable red lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "toggle_red_light",
        "description": "Toggle the red light on/off. Use when user asks to switch, toggle, or flip the red light.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    # Individual Blue Light Controls
    {
        "type": "function",
        "name": "turn_white_light_on",
        "description": "Turn the white light ON. Use when user asks to turn on white light, white lamp, or mentions white color lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "turn_white_light_off",
        "description": "Turn the white light OFF. Use when user asks to turn off white light, white lamp, or disable white lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "toggle_white_light",
        "description": "Toggle the white light on/off. Use when user asks to switch, toggle, or flip the white light.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    # Individual Green Light Controls
    {
        "type": "function",
        "name": "turn_green_light_on",
        "description": "Turn the green light ON. Use when user asks to turn on green light, green lamp, or mentions green color lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "turn_green_light_off",
        "description": "Turn the green light OFF. Use when user asks to turn off green light, green lamp, or disable green lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "toggle_green_light",
        "description": "Toggle the green light on/off. Use when user asks to switch, toggle, or flip the green light.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    # Individual Yellow Light Controls
    {
        "type": "function",
        "name": "turn_yellow_light_on",
        "description": "Turn the yellow light ON. Use when user asks to turn on yellow light, yellow lamp, or mentions yellow color lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "turn_yellow_light_off",
        "description": "Turn the yellow light OFF. Use when user asks to turn off yellow light, yellow lamp, or disable yellow lighting.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "toggle_yellow_light",
        "description": "Toggle the yellow light on/off. Use when user asks to switch, toggle, or flip the yellow light.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    # All Lights Controls
    {
        "type": "function",
        "name": "turn_all_lights_on",
        "description": "Turn ALL lights ON at once. Use when user asks to turn on all lights, every light, or all the lights.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "turn_all_lights_off",
        "description": "Turn ALL lights OFF at once. Use when user asks to turn off all lights, every light, all the lights, or wants darkness.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "toggle_all_lights",
        "description": "Toggle ALL lights on/off at once. Use when user asks to switch all lights, toggle everything, or flip all lights.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    # Status Functions
    {
        "type": "function",
        "name": "get_all_lights_status",
        "description": "Get the current status of all colored lights. Use when user asks about light status, which lights are on, or wants to check all lights.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
]

# Function mapping for easy execution
FUNCTION_MAP = {
    # Individual light controls
    "turn_red_light_on": turn_red_light_on,
    "turn_red_light_off": turn_red_light_off,
    "toggle_red_light": toggle_red_light,
    "turn_white_light_on": turn_white_light_on,
    "turn_white_light_off": turn_white_light_off,
    "toggle_white_light": toggle_white_light,
    "turn_green_light_on": turn_green_light_on,
    "turn_green_light_off": turn_green_light_off,
    "toggle_green_light": toggle_green_light,
    "turn_yellow_light_on": turn_yellow_light_on,
    "turn_yellow_light_off": turn_yellow_light_off,
    "toggle_yellow_light": toggle_yellow_light,
    # All lights controls
    "turn_all_lights_on": turn_all_lights_on,
    "turn_all_lights_off": turn_all_lights_off,
    "toggle_all_lights": toggle_all_lights,
    # Status functions
    "get_all_lights_status": get_all_lights_status,
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


# Voice command examples for testing
VOICE_COMMAND_EXAMPLES = [
    "Turn on the red light",
    "Turn off blue light",
    "Toggle green light",
    "Turn on all lights",
    "Turn off all the lights",
    "Switch all lights",
    "What's the status of all lights?",
    "Turn on yellow lamp",
    "Make it dark",  # (should turn off all lights)
]


def get_available_commands():
    """
    Returns a list of available voice commands for documentation.
    """
    return {
        "Individual Light Commands": [
            "Turn on [color] light",
            "Turn off [color] light",
            "Toggle [color] light",
            "Switch [color] light",
        ],
        "All Lights Commands": [
            "Turn on all lights",
            "Turn off all lights",
            "Toggle all lights",
            "Switch all lights",
            "Turn on every light",
            "Make it dark",
        ],
        "Status Commands": [
            "What's the light status?",
            "Check all lights",
            "Which lights are on?",
        ],
        "Available Colors": ["red", "blue", "green", "yellow"],
    }
