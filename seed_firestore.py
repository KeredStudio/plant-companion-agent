"""Seed script for populating initial plant catalog in Firestore."""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-7dbd053c0c16"

db = firestore.Client(project=PROJECT_ID)
PLANTS_COLLECTION = "plants"

INITIAL_PLANTS = [
    {
        "name": "Monstera Deliciosa",
        "name_lower": "monstera deliciosa",
        "species": "Monstera deliciosa",
        "light": "Bright indirect light",
        "watering_interval_days": 7,
        "difficulty": "Easy",
        "pet_friendly": False,
        "notes": "Loves humidity and developing fenestrated split leaves."
    },
    {
        "name": "Snake Plant",
        "name_lower": "snake plant",
        "species": "Dracaena trifasciata",
        "light": "Low to bright indirect light",
        "watering_interval_days": 14,
        "difficulty": "Beginner",
        "pet_friendly": False,
        "notes": "Extremely drought-tolerant and purifies indoor air."
    },
    {
        "name": "Spider Plant",
        "name_lower": "spider plant",
        "species": "Chlorophytum comosum",
        "light": "Medium to bright indirect light",
        "watering_interval_days": 6,
        "difficulty": "Easy",
        "pet_friendly": True,
        "notes": "Safe for cats and dogs; produces baby plantlets ('pups')."
    },
    {
        "name": "Boston Fern",
        "name_lower": "boston fern",
        "species": "Nephrolepis exaltata",
        "light": "Indirect filtered light",
        "watering_interval_days": 4,
        "difficulty": "Moderate",
        "pet_friendly": True,
        "notes": "Thrives in bathrooms or high humidity; soil should stay consistently moist."
    },
    {
        "name": "Fiddle Leaf Fig",
        "name_lower": "fiddle leaf fig",
        "species": "Ficus lyrata",
        "light": "Bright filtered light",
        "watering_interval_days": 8,
        "difficulty": "Challenging",
        "pet_friendly": False,
        "notes": "Sensitive to temperature drafts and being moved around."
    }
]


def seed():
    print(f"Connecting to Firestore with project '{PROJECT_ID}'...")
    collection_ref = db.collection(PLANTS_COLLECTION)
    
    # Check if collection already seeded
    existing = list(collection_ref.limit(1).stream())
    if existing:
        print("Plants collection already has documents. Clearing existing documents...")
        for doc in collection_ref.stream():
            doc.reference.delete()
        print("Cleared.")

    print(f"Seeding {len(INITIAL_PLANTS)} plant documents...")
    for plant in INITIAL_PLANTS:
        doc_ref = collection_ref.document()
        doc_ref.set(plant)
        print(f"  + Added: {plant['name']} (ID: {doc_ref.id})")
    
    print("✅ Firestore seeded successfully!")


if __name__ == "__main__":
    seed()
