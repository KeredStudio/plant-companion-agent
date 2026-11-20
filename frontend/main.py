import os
import uuid
import json
import logging
import google.auth
import google.auth.transport.requests
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESOURCE = os.environ["AGENT_ENGINE_RESOURCE_NAME"]
AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
LOCATION = RESOURCE.split("/locations/")[1].split("/")[0]

A2A_URL = (
    f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
    f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
)
_A2UI_MIME = "application/json+a2ui"

_creds, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def _auth_headers() -> dict[str, str]:
    _creds.refresh(google.auth.transport.requests.Request())
    return {
        "Authorization": f"Bearer {_creds.token}",
        "Content-Type": "application/json",
    }

app = FastAPI()

@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    logger.exception("Error handling request")
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )

_contexts: dict[str, str] = {}

def _extract_parts_from_task(task: dict) -> list[dict]:
    out = []

    # 1. First, check artifacts for A2UI data (primary output when A2UI is rendered)
    artifacts = task.get("artifacts") or []
    for art in artifacts:
        parts = art.get("parts") or []
        for p in parts:
            if isinstance(p, dict):
                data_wrap = p.get("data")
                if isinstance(data_wrap, dict):
                    meta = data_wrap.get("metadata") or {}
                    if meta.get("mimeType") == _A2UI_MIME:
                        out.append({"kind": "a2ui", "data": data_wrap.get("data")})
                    elif "data" in data_wrap:
                        out.append({"kind": "a2ui", "data": data_wrap["data"]})
                elif p.get("text"):
                    out.append({"kind": "text", "text": p["text"]})

    # If artifacts already supplied output (A2UI surface or text), return to avoid duplicating with history
    if out:
        return out

    # 2. If no artifacts were produced, extract the final agent message from history
    history = task.get("history") or []
    agent_messages = [msg for msg in history if isinstance(msg, dict) and msg.get("role") == "agent"]
    if agent_messages:
        latest_msg = agent_messages[-1]
        for p in latest_msg.get("parts") or []:
            if isinstance(p, dict):
                if p.get("kind") == "text" and p.get("text"):
                    out.append({"kind": "text", "text": p["text"]})
                elif p.get("text"):
                    out.append({"kind": "text", "text": p["text"]})
                elif p.get("data"):
                    dw = p.get("data")
                    if isinstance(dw, dict) and dw.get("metadata", {}).get("mimeType") == _A2UI_MIME:
                        out.append({"kind": "a2ui", "data": dw.get("data")})

    return out

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "web-user"
    context_id = _contexts.get(user_id)

    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"text": message}],
                "messageId": str(uuid.uuid4()),
            }
        }
    }
    if context_id:
        payload["params"]["message"]["contextId"] = context_id

    async with httpx.AsyncClient(headers=_auth_headers(), timeout=120) as client:
        resp = await client.post(A2A_URL, json=payload)
        resp_data = resp.json()

    task = resp_data.get("result", {})
    if task.get("contextId"):
        _contexts[user_id] = task["contextId"]

    parts = _extract_parts_from_task(task)

    if not parts:
        parts = [{"kind": "text", "text": "(The agent didn't return a reply.)"}]

    return JSONResponse({"parts": parts})

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
