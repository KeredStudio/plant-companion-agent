# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types


MODEL = "gemini-3.8-flash"


def get_weather(query: str) -> dict:
    """Fetch real-time weather and plant growing conditions (temperature, humidity, precipitation)
    for a location using the free Open-Meteo public API (no API key required).

    Args:
        query: The city name or location (e.g. 'San Francisco', 'Taipei', 'New York').

    Returns:
        A dictionary with real temperature (°C), relative humidity (%), precipitation, and local weather.
    """
    import json
    import urllib.parse
    import urllib.request

    try:
        # Step 1: Geocode city name to latitude and longitude
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search?"
            f"name={urllib.parse.quote(query.strip())}&count=1&language=en&format=json"
        )
        geo_req = urllib.request.Request(geo_url, headers={"User-Agent": "PlantCompanion/1.0"})
        with urllib.request.urlopen(geo_req, timeout=10) as resp:
            geo_data = json.loads(resp.read().decode("utf-8"))

        results = geo_data.get("results")
        if not results:
            return {"status": "not_found", "message": f"Could not find coordinates for '{query}'."}

        place = results[0]
        lat, lon = place["latitude"], place["longitude"]
        place_name = f"{place.get('name')}, {place.get('country', '')}"

        # Step 2: Fetch current weather metrics vital for indoor/outdoor plants
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,relative_humidity_2m,precipitation,weather_code"
        )
        weather_req = urllib.request.Request(weather_url, headers={"User-Agent": "PlantCompanion/1.0"})
        with urllib.request.urlopen(weather_req, timeout=10) as resp:
            weather_data = json.loads(resp.read().decode("utf-8"))

        current = weather_data.get("current", {})
        temp_c = current.get("temperature_2m")
        temp_f = round((temp_c * 9 / 5) + 32, 1) if temp_c is not None else None
        humidity = current.get("relative_humidity_2m")
        precip = current.get("precipitation")

        return {
            "status": "success",
            "location": place_name,
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "humidity_percent": humidity,
            "precipitation_mm": precip,
            "growing_environment_advice": (
                "Ideal indoor temperature" if temp_c and 18 <= temp_c <= 26 else
                "Low temperature alert: protect tropical plants" if temp_c and temp_c < 15 else
                "High temperature alert: monitor soil moisture and mist leaves"
            ),
        }
    except Exception as exc:
        return {"status": "error", "message": f"Weather lookup failed: {exc}"}



def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


from app.firestore_service import (
    add_plant_to_catalog,
    get_plant_catalog,
    search_plant,
    update_plant_watering,
    update_plant_fertilizer,
)


def list_plants() -> list[dict]:
    """Retrieve all available plants in the catalog from the Firestore database.

    Returns:
        A list of plant dictionaries containing name, light requirements, watering interval, etc.
    """
    return get_plant_catalog()


def lookup_plant(plant_name: str) -> dict:
    """Look up care details for a specific plant by its common name.

    Args:
        plant_name: Common name of the plant (e.g. 'Monstera Deliciosa', 'Snake Plant').

    Returns:
        A dictionary with the plant's care guidelines, or an error status if not found.
    """
    result = search_plant(plant_name)
    if result:
        return result
    return {"status": "not_found", "message": f"No plant named '{plant_name}' found in the catalog."}


def record_new_plant(
    name: str,
    species: str,
    light: str,
    watering_interval_days: int,
    difficulty: str,
    pet_friendly: bool,
    notes: str = "",
) -> dict:
    """Add a new plant entry to the Firestore plant database.

    Args:
        name: Common name of the plant.
        species: Botanical/Latin species name.
        light: Sunlight requirement description (e.g., 'Bright indirect light').
        watering_interval_days: How often to water in days (integer).
        difficulty: Care difficulty level ('Beginner', 'Easy', 'Moderate', 'Challenging').
        pet_friendly: True if safe for pets (dogs/cats), False otherwise.
        notes: Extra tips or care notes.

    Returns:
        The newly created plant record with its generated Firestore ID.
    """
    return add_plant_to_catalog(
        name=name,
        species=species,
        light=light,
        watering_interval_days=watering_interval_days,
        difficulty=difficulty,
        pet_friendly=pet_friendly,
        notes=notes,
    )


def log_watering(plant_name: str, notes: str = "") -> dict:
    """Log that a plant has just been watered. Updates the plant's last_watered_at
    timestamp and calculates the next watering due date in Firestore.

    Args:
        plant_name: The common name of the plant that was watered (e.g. 'Monstera Deliciosa', 'Snake Plant').
        notes: Optional observation or note (e.g. 'added liquid fertilizer').

    Returns:
        A dictionary with the updated watering status and next due date.
    """
    return update_plant_watering(name=plant_name, notes=notes)


def diagnose_plant_health(plant_name: str, symptoms: str) -> dict:
    """Diagnose a plant disease, pest infestation, or environmental problem based on symptoms
    (e.g. yellowing leaves, brown crispy tips, spider mites, drooping stems).

    Args:
        plant_name: Name of the plant experiencing issues (e.g. 'Monstera Deliciosa', 'Fiddle Leaf Fig').
        symptoms: Description of the observed symptoms or leaf conditions.

    Returns:
        A structured diagnosis dictionary including likely cause, emergency treatment, and recovery timeline.
    """
    sym = symptoms.lower()
    if "yellow" in sym or "黃" in sym:
        cause = "Overwatering or root saturation causing oxygen starvation (Root Stress / Chlorosis)."
        treatment = "Check soil moisture with a wooden skewer. Stop watering until top 2-3 inches are dry. Ensure drainage holes are clear."
    elif "brown" in sym or "crisp" in sym or "焦" in sym or "乾" in sym:
        cause = "Low atmospheric humidity, underwatering, or direct sunlight scorch."
        treatment = "Increase ambient humidity (50-60%), trim severely damaged tips with sterilized shears, and relocate away from heat vents or harsh direct sun."
    elif "mite" in sym or "web" in sym or "蟲" in sym or "蛛" in sym or "white" in sym:
        cause = "Pest infestation (Spider Mites, Mealybugs, or Fungus Gnats)."
        treatment = "Isolate immediately. Wipe foliage with a gentle solution of diluted neem oil or insecticidal soap every 5-7 days."
    elif "droop" in sym or "垂" in sym:
        cause = "Severe dehydration or root shock due to rapid temperature change."
        treatment = "Perform bottom-watering for 30 minutes, or shelter away from cold winter drafts."
    else:
        cause = "Nutrient imbalance or seasonal adjustment shock."
        treatment = "Inspect roots for rot, ensure bright indirect light, and pause heavy fertilization during winter."

    return {
        "status": "success",
        "plant_name": plant_name,
        "symptoms": symptoms,
        "likely_cause": cause,
        "emergency_action": treatment,
        "recovery_time": "1 to 3 weeks with proper adjustment",
        "winter_tip": "Winter light is weaker; reduce watering frequency and keep leaves clean from dust."
    }


def calculate_repotting_and_soil(plant_name: str, current_pot_diameter_cm: float) -> dict:
    """Calculate the ideal new pot dimensions and tailored soil/medium recipe
    (peat moss, perlite, pumice, bark) when repotting a plant.

    Args:
        plant_name: Name of the plant to repot (e.g. 'Monstera', 'Snake Plant', 'Succulent', 'Aroid').
        current_pot_diameter_cm: Current pot diameter in centimeters (e.g. 15.0).

    Returns:
        A dictionary with recommended pot size, drainage requirement, and exact soil mix ratios.
    """
    new_pot = current_pot_diameter_cm + 3.0 if current_pot_diameter_cm <= 15 else current_pot_diameter_cm + 5.0
    p_lower = plant_name.lower()

    if "snake" in p_lower or "succulent" in p_lower or "cactus" in p_lower or "虎尾蘭" in p_lower or "多肉" in p_lower:
        recipe = "Fast-Draining Mineral Mix: 50% Pumice/Perlite, 30% Succulent Soil, 20% Coarse Sand."
        drainage = "Maximum drainage essential; unglazed terracotta pot recommended."
    elif "monstera" in p_lower or "fig" in p_lower or "pothos" in p_lower or "龜背" in p_lower or "琴葉" in p_lower:
        recipe = "Chunky Aroid Mix: 40% Peat moss/Coco coir, 30% Orchid Bark, 20% Perlite, 10% Worm castings."
        drainage = "High porosity with drainage holes to prevent root rot."
    else:
        recipe = "All-Purpose Indoor Mix: 60% Quality Potting Soil, 20% Perlite, 20% Compost."
        drainage = "Standard drainage pot with saucer."

    return {
        "status": "success",
        "plant_name": plant_name,
        "current_pot_size_cm": current_pot_diameter_cm,
        "recommended_new_pot_cm": new_pot,
        "pot_upsize_guide": f"Upgrade from {current_pot_diameter_cm}cm to {new_pot}cm diameter pot.",
        "soil_recipe": recipe,
        "drainage_notes": drainage,
        "best_season": "Spring through early Summer (avoid repotting in deep winter unless emergency rot)."
    }


def log_fertilizing(plant_name: str, fertilizer_type: str = "Balanced Liquid Fertilizer", notes: str = "") -> dict:
    """Log that a plant has been fertilized. Updates Firestore and calculates next due date
    taking seasonal dormancy (winter vs active growth) into consideration.

    Args:
        plant_name: Common name of the plant (e.g. 'Monstera Deliciosa').
        fertilizer_type: Type of fertilizer applied (e.g. 'Liquid 10-10-10', 'Slow-release granules').
        notes: Optional extra observation.

    Returns:
        A dictionary with the updated fertilizer schedule and seasonal advisory.
    """
    return update_plant_fertilizer(name=plant_name, fertilizer_type=fertilizer_type, notes=notes)


def evaluate_room_sunlight(window_facing_direction: str) -> dict:
    """Evaluate indoor lighting conditions based on window orientation (North, South, East, West)
    and recommend suitable indoor plants.

    Args:
        window_facing_direction: The direction the window faces ('North', 'South', 'East', 'West' or '東', '西', '南', '北').

    Returns:
        Light level description, daily sun exposure hours, and list of recommended plants.
    """
    d = window_facing_direction.lower()
    if "south" in d or "南" in d:
        light = "Bright Direct to High Indirect Light"
        hours = "5 to 7 hours of abundant daylight"
        plants = ["Fiddle Leaf Fig", "Bird of Paradise", "Cactus & Succulents", "Citrus", "Jade Plant"]
    elif "east" in d or "東" in d:
        light = "Gentle Morning Direct + Medium Indirect Light"
        hours = "3 to 4 hours of gentle morning sun"
        plants = ["Monstera Deliciosa", "Calathea (Prayer Plant)", "Boston Fern", "Peace Lily", "Anthurium"]
    elif "west" in d or "西" in d:
        light = "Intense Afternoon Sun + High Ambient Light"
        hours = "4 to 6 hours of warm afternoon sun"
        plants = ["Snake Plant", "ZZ Plant", "Rubber Tree (Ficus Elastica)", "Pothos", "Dracaena"]
    else:  # North
        light = "Low to Gentle Medium Indirect Light (No harsh rays)"
        hours = "Consistent low-intensity ambient light"
        plants = ["Cast Iron Plant", "ZZ Plant", "Snake Plant", "Chinese Evergreen (Aglaonema)", "Heartleaf Philodendron"]

    return {
        "status": "success",
        "direction": window_facing_direction,
        "light_quality": light,
        "sunlight_hours": hours,
        "recommended_plants": plants,
        "winter_tip": "In winter, move plants 30-50 cm closer to windows to capture limited daylight."
    }


def geocode_address(address: str) -> dict:
    """Convert an address, neighborhood, or city into geographical coordinates (latitude and longitude)
    using the Google Maps Geocoding API.

    Args:
        address: The address or location string to geocode (e.g. '1600 Amphitheatre Pkwy, Mountain View, CA' or 'San Francisco').

    Returns:
        A dictionary with formatted address and coordinates (latitude, longitude).
    """
    import json
    import os
    import urllib.parse
    import urllib.request
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"status": "error", "message": "GOOGLE_MAPS_API_KEY environment variable is not configured."}

    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json?"
        f"address={urllib.parse.quote(address)}&key={api_key}"
    )
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if data.get("status") != "OK" or not data.get("results"):
            return {"status": "not_found", "message": f"Could not geocode address: {address}"}

        first_res = data["results"][0]
        location = first_res["geometry"]["location"]
        return {
            "status": "success",
            "formatted_address": first_res.get("formatted_address"),
            "latitude": location["lat"],
            "longitude": location["lng"],
        }
    except Exception as exc:
        return {"status": "error", "message": f"Geocoding request failed: {exc}"}


def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "florist",
    radius_meters: float = 5000.0,
    max_results: int = 5,
) -> dict:
    """Find nearby places (such as florists, nurseries, garden centers, home improvement stores)
    around a latitude and longitude using Google Places API (New).

    Args:
        latitude: Center latitude coordinate.
        longitude: Center longitude coordinate.
        place_type: Type of place to search for (e.g., 'florist', 'home_goods_store', 'store', 'park').
        radius_meters: Search radius in meters (default is 5000 meters / 5 km).
        max_results: Maximum number of places to return (up to 20).

    Returns:
        A dictionary with a list of matching places containing name, formatted address, and location coordinates.
    """
    import json
    import os
    import urllib.request
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"status": "error", "message": "GOOGLE_MAPS_API_KEY environment variable is not configured."}

    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.types",
    }
    payload = json.dumps({
        "includedTypes": [place_type],
        "maxResultCount": min(max_results, 20),
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius_meters,
            }
        },
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        places = []
        for p in data.get("places", []):
            places.append({
                "name": p.get("displayName", {}).get("text", "Unknown"),
                "address": p.get("formattedAddress"),
                "location": p.get("location"),
                "types": p.get("types", []),
            })

        return {
            "status": "success",
            "count": len(places),
            "places": places,
        }
    except Exception as exc:
        return {"status": "error", "message": f"Places search failed: {exc}"}


def generate_plant_image(prompt: str, tool_context=None) -> dict:
    """Generate an illustration or photo for a plant using Google's gemini-3.1-flash-lite-image
    generative model in the global region. The image is saved to the local artifacts panel and
    uploaded to the public Cloud Storage bucket so it can be viewed publicly and embedded in A2UI cards.

    Args:
        prompt: A descriptive text prompt of the plant to generate (e.g. 'A lush Monstera Deliciosa with fenestrated leaves in a terracotta pot').
        tool_context: ToolContext passed automatically by the ADK runtime.

    Returns:
        A dictionary with public_url, artifact_name, and status.
    """
    import uuid
    import google.genai as genai
    from google.cloud import storage

    bucket_name = "plant-companion-assets-qwiklabs-gcp-03-7dbd053c0c16"
    project_id = "qwiklabs-gcp-03-7dbd053c0c16"

    try:
        client = genai.Client(vertexai=True, project=project_id, location="global")
        resp = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=f"Botanical illustration of: {prompt}. High quality, clean background.",
        )
        img_bytes = None
        for candidate in resp.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    img_bytes = part.inline_data.data
                    break
            if img_bytes:
                break

        if not img_bytes:
            return {"status": "error", "message": "No image data returned from generative model."}

        # 1. Save artifact if tool_context is provided
        artifact_filename = f"plant_{uuid.uuid4().hex[:8]}.png"
        if tool_context and hasattr(tool_context, "save_artifact"):
            try:
                tool_context.save_artifact(filename=artifact_filename, content=img_bytes)
            except Exception as e:
                pass

        # 2. Upload image bytes to public Cloud Storage bucket
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob_path = f"generated/{artifact_filename}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(img_bytes, content_type="image/png")
        public_url = f"https://storage.googleapis.com/{bucket_name}/{blob_path}"

        return {
            "status": "success",
            "public_url": public_url,
            "artifact_name": artifact_filename,
            "description": f"Generated image for: {prompt}",
        }
    except Exception as exc:
        return {"status": "error", "message": f"Image generation failed: {exc}"}


from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from app.a2ui_utils import a2ui_callback
from a2ui.inference_formats.direct_json.prompt_generator import DirectJsonPromptGenerator
from a2ui.core.basic_catalog.v0_8 import BasicCatalog

# Build system prompt for A2UI
_a2ui_generator = DirectJsonPromptGenerator([BasicCatalog()])
_a2ui_schema_prompt = _a2ui_generator.generate()

AGENT_SYSTEM_PROMPT = f"""You are Plant Companion (Winter ❄️), an expert urban plant care assistant with deep botanical and horticultural intelligence.
You help users manage and care for indoor greenery, diagnose plant diseases and pests (diagnose_plant_health),
calculate custom repotting pot dimensions and soil recipes (calculate_repotting_and_soil),
log watering events (log_watering) and seasonal fertilizing schedules (log_fertilizing),
evaluate indoor window lighting orientation (evaluate_room_sunlight),
find local plant nurseries/florists with Google Maps (find_nearby_places),
generate botanical images (generate_plant_image), and manage the Firestore plant catalog.

When presenting plant information, care guides, weather advisories, diagnosis results, or recipes,
you may output structured A2UI JSON components using version 0.8 to create clean, readable cards and tables.
Keep surfaces simple: ONE Card > ONE Column > a few Text rows or Image.
When an image is generated, display it using an Image component with its public https URL.

{_a2ui_schema_prompt}
"""


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: after each turn, send the session to Memory Bank for extraction."""
    try:
        await callback_context.add_session_to_memory()
    except Exception:
        pass
    return None


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=AGENT_SYSTEM_PROMPT,
    tools=[
        PreloadMemoryTool(),
        list_plants,
        lookup_plant,
        record_new_plant,
        log_watering,
        log_fertilizing,
        diagnose_plant_health,
        calculate_repotting_and_soil,
        evaluate_room_sunlight,
        geocode_address,
        find_nearby_places,
        get_weather,
        get_current_time,
        generate_plant_image,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)

