from dotenv import load_dotenv
load_dotenv()

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, TEXT, IndexModel
import os

# ── CONNECTION ────────────────────────────────────────────────────────────────
# Set the MONGO_URI environment variable in your shell or Railway dashboard.
# Example Atlas URI:
#   mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
#
# For local development you can also use:
#   MONGO_URI=mongodb://localhost:27017

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
)
DB_NAME = os.getenv("DB_NAME", "smart_notes")

client = AsyncIOMotorClient(MONGO_URI)
db     = client[DB_NAME]

notes_collection    = db["notes"]
counters_collection = db["counters"]


# ── AUTO-INCREMENT ID ─────────────────────────────────────────────────────────
# Uses an atomic findOneAndUpdate so concurrent requests never get the same ID.

async def get_next_id() -> int:
    result = await counters_collection.find_one_and_update(
        {"_id": "note_id"},          # the counter document
        {"$inc": {"seq": 1}},        # atomically increment by 1
        upsert=True,                 # create it on first use
        return_document=True         # return the updated doc (not the old one)
    )
    return result["seq"]


# ── INDEXES ───────────────────────────────────────────────────────────────────
# Called once at startup. Safe to call repeatedly — MongoDB is idempotent here.

async def create_indexes():
    await notes_collection.create_indexes([
        IndexModel([("id", ASCENDING)], unique=True),
        IndexModel(
            [("title", TEXT), ("content", TEXT), ("summary", TEXT)],
            name="notes_text_search"
        )
    ])