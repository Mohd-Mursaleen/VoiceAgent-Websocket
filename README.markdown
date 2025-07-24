# Voice Agent Package

This package provides a FastAPI WebSocket server that enables real-time interaction with OpenAI's realtime voice agent API. It allows you to connect and communicate with the voice agent using WebSockets.

## Features
- Websocket handling for real-time communication
- Audio streaming support

## Setup with Poetry

1. Install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:

```bash
cd voice_agent_package
poetry install
```

3. Configure environment variables by copying and editing .env.example:

```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Start the server:

```bash
poetry run start
```

Alternatively, you can use:

```bash
poetry run uvicorn voice_agent_package.main:app --host 0.0.0.0 --port 8000
```

## Testing the Setup

1. Test the health endpoint:

```bash
curl http://localhost:8000/health
```

You should see: `{"status":"healthy","version":"1.0.0"}`

2. Test the WebSocket connection:

Use a WebSocket client to connect to `ws://localhost:8000/audio-stream/`
## Usage

The main WebSocket endpoint for interacting with the OpenAI voice agent is at `audio-stream/`. You can connect to this endpoint using a WebSocket client and send/receive audio data in real-time. The package handles the connection to OpenAI's API and manages the audio streaming, allowing for seamless interaction with the voice agent.