# Plant Companion 🌿

**Plant Companion** is an intelligent conversational agent designed for urban plant enthusiasts to care for and nurture their home greenery with a catalog of plants, care reminders, and botanical utilities.

Built with Google ADK, deployed to Vertex AI Agent Platform (Agent Runtime / Reasoning Engine) and served via a Cloud Run web chat frontend supporting the A2A protocol and rich A2UI interactive cards.

---

## Features

- **Plant Care & Inventory Database**: Backed by Firestore for cataloging indoor plants (light, watering schedule, difficulty, pet toxicity).
- **Watering Log & Tracker**: Records watering events in Firestore and automatically calculates next due dates.
- **Botanical Illustrations**: Generates vintage watercolor botanical illustrations using `gemini-3.1-flash-lite-image` and hosts them on Cloud Storage.
- **Local Weather & Care Advisory**: Fetches real-time temperature and humidity via Open-Meteo API to give actionable advice (e.g. frost protection).
- **Nursery & Florist Finder**: Connects with Google Maps Geocoding & Places API (New) to locate nearby plant shops and garden centers.
- **Rich A2UI Display**: Renders responses as rich display cards, tables, and images.
- **Interactive Chat Frontend**: Web interface featuring a drawer hamburger menu to review recent conversation history.

---

## Architecture & Project Structure

```
my-agent/
├── app/                       # Core agent implementation
│   ├── agent.py               # ReAct agent, tools, callbacks, and A2UI schema
│   ├── a2ui_utils.py          # A2UI callback and message wrapper
│   └── firestore_service.py   # Firestore CRUD helpers
├── frontend/                  # Web Chat UI & A2A Proxy
│   ├── main.py                # FastAPI proxy communicating over A2A JSON-RPC
│   ├── static/index.html      # Responsive UI with A2UI renderer & history drawer
│   └── requirements.txt       # Frontend dependencies
├── seed_firestore.py          # Seed initial plant catalog
└── pyproject.toml             # Python project dependencies
```

---

## Quick Start (Local Run)

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure environment**:
   Copy `.env.example` to `.env` and provide your `GOOGLE_MAPS_API_KEY` (and `PROJECT_ID`).

3. **Run local agent**:
   ```bash
   agents-cli run
   ```

4. **Run frontend locally**:
   ```bash
   cd frontend
   export AGENT_ENGINE_RESOURCE_NAME="<your-reasoning-engine-resource-name>"
   export AGENT_DIRECTORY="app"
   uvicorn main:app --port 8080
   ```
