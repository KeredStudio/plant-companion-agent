"""Firestore client and service for plant-companion."""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-7dbd053c0c16"

# Initialize Firestore client with hardcoded project ID
db = firestore.Client(project=PROJECT_ID)
PLANTS_COLLECTION = "plants"


def get_plant_catalog() -> list[dict]:
    """Retrieve all plants from the Firestore catalog."""
    docs = db.collection(PLANTS_COLLECTION).stream()
    plants = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        plants.append(data)
    return plants


def search_plant(name: str) -> dict | None:
    """Search for a specific plant by common name."""
    query = db.collection(PLANTS_COLLECTION).where("name_lower", "==", name.lower().strip()).limit(1).stream()
    for doc in query:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None


def add_plant_to_catalog(
    name: str,
    species: str,
    light: str,
    watering_interval_days: int,
    difficulty: str,
    pet_friendly: bool,
    notes: str = ""
) -> dict:
    """Add a new plant to the Firestore catalog."""
    plant_data = {
        "name": name,
        "name_lower": name.lower().strip(),
        "species": species,
        "light": light,
        "watering_interval_days": watering_interval_days,
        "difficulty": difficulty,
        "pet_friendly": pet_friendly,
        "notes": notes,
    }
    doc_ref = db.collection(PLANTS_COLLECTION).document()
    doc_ref.set(plant_data)
    plant_data["id"] = doc_ref.id
    return plant_data


def update_plant_watering(name: str, notes: str = "") -> dict:
    """Record a watering event for a plant and update its Firestore record."""
    import datetime

    query = db.collection(PLANTS_COLLECTION).where("name_lower", "==", name.lower().strip()).limit(1).stream()
    doc_snapshot = None
    for doc in query:
        doc_snapshot = doc
        break

    if not doc_snapshot:
        return {"status": "error", "message": f"Plant '{name}' not found in catalog."}

    plant_data = doc_snapshot.to_dict()
    interval = plant_data.get("watering_interval_days", 7)

    now = datetime.datetime.now(datetime.timezone.utc)
    next_due = now + datetime.timedelta(days=interval)

    update_payload = {
        "last_watered_at": now.isoformat(),
        "next_watering_due": next_due.isoformat(),
    }
    if notes:
        update_payload["last_watering_notes"] = notes

    db.collection(PLANTS_COLLECTION).document(doc_snapshot.id).update(update_payload)

    plant_data.update(update_payload)
    plant_data["id"] = doc_snapshot.id
    return {
        "status": "success",
        "plant_name": plant_data.get("name"),
        "last_watered_at": now.strftime("%Y-%m-%d %H:%M UTC"),
        "next_watering_due": next_due.strftime("%Y-%m-%d"),
        "watering_interval_days": interval,
    }


def update_plant_fertilizer(name: str, fertilizer_type: str, notes: str = "") -> dict:
    """Record a fertilizing event for a plant and calculate next schedule based on season."""
    import datetime

    query = db.collection(PLANTS_COLLECTION).where("name_lower", "==", name.lower().strip()).limit(1).stream()
    doc_snapshot = None
    for doc in query:
        doc_snapshot = doc
        break

    if not doc_snapshot:
        return {"status": "error", "message": f"Plant '{name}' not found in catalog."}

    now = datetime.datetime.now(datetime.timezone.utc)
    month = now.month
    # Spring/Summer (April-September) -> 14-30 days; Autumn/Winter (October-March) -> Dormant / 60+ days
    is_dormant_season = month in [10, 11, 12, 1, 2, 3]
    interval = 60 if is_dormant_season else 21
    next_due = now + datetime.timedelta(days=interval)

    update_payload = {
        "last_fertilized_at": now.isoformat(),
        "next_fertilizer_due": next_due.isoformat(),
        "fertilizer_type": fertilizer_type,
    }
    if notes:
        update_payload["last_fertilizer_notes"] = notes

    db.collection(PLANTS_COLLECTION).document(doc_snapshot.id).update(update_payload)

    return {
        "status": "success",
        "plant_name": doc_snapshot.to_dict().get("name"),
        "last_fertilized_at": now.strftime("%Y-%m-%d"),
        "fertilizer_type": fertilizer_type,
        "next_fertilizer_due": next_due.strftime("%Y-%m-%d"),
        "seasonal_advice": (
            "Winter/Dormant season: Avoid over-fertilizing. Dilute to half-strength or pause until Spring."
            if is_dormant_season else
            "Active growing season: Regular feeding supports vigorous leaf and root development."
        ),
    }


