import json
import logging
import asyncio
from app.client.client import OpenAIWebSocketClient

logger = logging.getLogger(__name__)

async def send_tool_result(openai_client, call_id: str, result: dict):
    """Send function call result back to OpenAI Realtime API."""
    try:
        # Create a conversation item with the function call output
        message = {
            "type": "conversation.item.create",
            "item": {
                "type": "function_call_output",
                "call_id": call_id,
                "output": json.dumps(result) if isinstance(result, dict) else str(result)
            }
        }
        
        await openai_client.send(json.dumps(message))
        logger.info(f"Tool result sent successfully for call_id: {call_id}")
        
        # After adding the function result, trigger a response
        response_message = {
            "type": "response.create"
        }
        await openai_client.send(json.dumps(response_message))
        
    except Exception as e:
        logger.error(f"Error sending tool result: {e}")