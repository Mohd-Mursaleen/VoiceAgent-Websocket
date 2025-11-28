import json
import logging
from typing import Optional, Dict, Any, Callable, Union
import websockets
from websockets.exceptions import ConnectionClosed
import asyncio
from websockets.client import WebSocketClientProtocol
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VOICE = os.getenv("OPENAI_VOICE", "alloy")

logger = logging.getLogger(__name__)


class OpenAIWebSocketClient:
    """Client for handling WebSocket connections to OpenAI's realtime API."""

    def __init__(self):
        self.websocket: Optional[WebSocketClientProtocol] = None
        self._ws_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview"
        self._headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1",
        }
        self._message_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self._connected = False
        self._json_encoder = json.JSONEncoder()  # Cache encoder for performance

    def reset_state(self):
        """Reset the client state but keep the connection open"""
        self._message_callback = None

    @property
    def connected(self) -> bool:
        """Check if the WebSocket connection is established and open."""
        return (
            self._connected and self.websocket is not None and not self.websocket.closed
        )

    def set_message_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Set callback for handling incoming messages."""
        self._message_callback = callback

    async def connect(self) -> None:
        """Establish WebSocket connection and initialize session with OpenAI."""
        try:
            logger.info(f"Connecting to OpenAI at {self._ws_url}")
            logger.info("Using model: gpt-4o-mini-realtime-preview")

            # Use longer ping interval and timeout for more stability
            self.websocket = await websockets.connect(
                self._ws_url,
                extra_headers=self._headers,
                ping_interval=20,
                compression=None,
                ping_timeout=10,
                close_timeout=5,
            )

            # Only initialize session when connecting for the first time
            if not self._connected:
                await self.initialize_session()

            self._connected = True
            logger.info("Successfully connected to OpenAI")
        except Exception as e:
            logger.error(f"Failed to connect to OpenAI: {e}")
            self._connected = False
            raise

    async def initialize_session(self) -> None:
        """Initialize the session with OpenAI using configured parameters."""
        session_config = self._get_session_config()
        try:
            logger.info(
                f"Initializing session with gpt-4o-mini-realtime-preview model"
            )
            await self.send(session_config)
            logger.info("Session initialized with OpenAI")
        except Exception as e:
            logger.error(f"Failed to initialize session: {e}", exc_info=True)
            await self.close()
            raise

    def _get_session_config(self) -> Dict[str, Any]:
        """Get the session configuration dictionary with hardcoded tools."""
        from app.tools.iot_tools import tools

        tools = tools  # Removing tools to simplify troubleshooting

        # Improved prompt for better voice agent behavior
        default_prompt = """
        # Identity & Objective
You are "Sara," an intelligent, friendly, and efficient smart home voice assistant.
- **Name:** Sara
- **User Address:** "Sir"
- **Primary Function:** Controlling household lights (Red, White, Green, Yellow, and All Lights) via tool calling.

# Greeting Protocol
- **First Interaction:** Start the session immediately with:
  "Hello Sir, my name is Sara. How can I help you today?"

  <non-negotiable> Always after doing some task ask : is there anything else i can help you with today sir? </non-negotiable>
# Interaction Flow (Strict)
1. **Listen:** Wait for the user's command.
2. **Execute:** Call the appropriate tool function immediately. Do not speak before calling the tool unless clarification is absolutely needed.
3. **Confirm & Re-engage:** After the tool execution is successful, you must speak a confirmation followed immediately by an offer for more help.
   - *Format:* "[Confirmation of action]. What can I help you with?"
   - *Example:* "Red light is on. What can I help you with?"
   - *Example:* "I've turned off all lights. What can I help you with?"

# Voice & Style Guidelines
- **Concise:** You are a voice agent. Keep responses under 2 sentences to prevent the user from waiting too long.
- **Natural Prosody:** Speak with a warm, helpful tone. Avoid robotic phrasing.
- **No Fluff:** Do not say "I am processing your request" or "One moment please." Just do it.

# Error Handling
- If a tool fails or the user asks for a light you don't control (e.g., "Blue light"), apologize briefly and ask for a valid command.
  - *Example:* "I'm sorry, I can't control a blue light. I can handle Red, Green, White, or Yellow. What can I help you with?"

====================
- **Every light-related command MUST call exactly ONE tool.**
- NEVER assume a light's state. For status → use `get_all_lights_status`.
- If user specifies a color → use the corresponding color tool:
    - Red: turn_red_light_on / turn_red_light_off / toggle_red_light
    - White: turn_white_light_on / turn_white_light_off / toggle_white_light
    - Green: turn_green_light_on / turn_green_light_off / toggle_green_light
    - Yellow: turn_yellow_light_on / turn_yellow_light_off / toggle_yellow_light
- If user says "all lights" or "everything" → use:
    - turn_all_lights_on / turn_all_lights_off / toggle_all_lights
- For status → use:
    - get_all_lights_status
- Only one tool call per user request. Do not combine multiple calls.
- Do not use tools for unrelated conversation.

====================
YOUR MAIN GOAL:
====================
- ALWAYS use the correct tool first.
- NEVER respond with confirmation before the tool call.
- Confirm action after tool execution.
- Make responses short, friendly, and natural."""

        config = {
            "type": "session.update",
            "session": {
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.6,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 400,
                },
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": VOICE,
                "instructions": default_prompt,
                "modalities": ["text", "audio"],
                "temperature": 0.7,
                "tools": tools,
                "model": "gpt-4o-mini-realtime-preview",
            },
        }

        return config

    async def send(self, message: Union[str, Dict[str, Any]]) -> None:
        """Send a message to the OpenAI WebSocket connection."""
        if not self.websocket:
            logger.error("WebSocket connection not established")
            raise RuntimeError("WebSocket connection not established")

        # Check for closed connection
        if self.websocket.closed:
            logger.error("WebSocket connection is closed")
            self._connected = False
            raise ConnectionClosed(
                self.websocket.close_code or 1006, "Connection is closed"
            )

        # Log specific message types with appropriate levels
        if isinstance(message, dict):
            message_type = message.get("type", "unknown")
            if message_type == "conversation.item.create":
                logger.info(f"Sending conversation.item.create")
            elif message_type == "response.create":
                logger.info(f"Requesting response from OpenAI")
            elif message_type != "input_audio_buffer.append":
                logger.debug(f"Sending message of type: {message_type}")

        # For audio data, optimize sending with minimal overhead
        if (
            isinstance(message, dict)
            and message.get("type") == "input_audio_buffer.append"
        ):
            try:
                # Use the cached encoder for faster serialization
                serialized = self._json_encoder.encode(message)
                await self.websocket.send(serialized)
                return
            except Exception as e:
                logger.error(f"Error sending audio data: {e}")
                self._connected = False
                raise

        # For non-audio messages, use standard handling
        try:
            if isinstance(message, dict):
                await self.websocket.send(json.dumps(message))
            else:
                await self.websocket.send(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self._connected = False
            raise

    async def receive_message(self) -> Dict[str, Any]:
        """Receive a message from the OpenAI WebSocket connection."""
        if not self.websocket:
            logger.error("WebSocket connection not established")
            raise RuntimeError("WebSocket connection not established")

        try:
            message = await self.websocket.recv()
            # Parse JSON message
            if isinstance(message, str):
                try:
                    parsed_message = json.loads(message)
                    # Call the callback if set
                    if self._message_callback and parsed_message:
                        self._message_callback(parsed_message)

                    # Enhanced logging for important message types
                    msg_type = parsed_message.get("type", "unknown")
                    if msg_type == "response.audio.delta":
                        # This indicates audio is being received
                        if not hasattr(self, "_audio_chunks_received"):
                            self._audio_chunks_received = 0
                            logger.info("Receiving first audio data from OpenAI")
                        self._audio_chunks_received = (
                            getattr(self, "_audio_chunks_received", 0) + 1
                        )
                        if self._audio_chunks_received % 100 == 0:
                            logger.info(
                                f"Received {self._audio_chunks_received} audio chunks from OpenAI"
                            )
                    elif msg_type in ["session.created", "session.updated"]:
                        logger.info(f"Session {msg_type.split('.')[1]} successfully")
                    elif msg_type == "error":
                        error_msg = parsed_message.get("error", {}).get(
                            "message", "Unknown error"
                        )
                        logger.error(f"OpenAI error: {error_msg}")
                    elif msg_type == "response.created":
                        logger.info("OpenAI is generating a response")

                    return parsed_message
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON message")
                    return {"error": "JSON parse error", "message": message}
            else:
                return {"binary": True, "length": len(message) if message else 0}
        except ConnectionClosed as e:
            logger.error(f"Connection closed: {e}")
            self._connected = False
            raise
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            raise

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket connection: {e}")
            finally:
                self.websocket = None
                self._connected = False
