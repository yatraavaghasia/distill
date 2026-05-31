import os
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import notes_collection, get_next_id, create_indexes

app = FastAPI(
    title="Smart Notes API",
    description="FastAPI + MongoDB Atlas backend with AI summarisation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()


# ── STARTUP ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    await create_indexes()


# ── SCHEMAS ───────────────────────────────────────────────────────────────────

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str] = []


# ── HELPERS ───────────────────────────────────────────────────────────────────

# MongoDB returns documents with a '_id' ObjectId field that Pydantic can't
# serialise. This helper strips it before returning to the client.
def clean(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


# ── AI BACKGROUND WORKER ──────────────────────────────────────────────────────

async def generate_ai_summary_and_tags(note_id: int, note_content: str):
    system_instruction = """
    Analyze the following note content.
    1. Provide a short 1-sentence summary.
    2. Provide up to 3 relevant one-word tags separated by commas.
       Tags should reflect the theme or subject — e.g. "philosophy", "finance", "travel".
       Do NOT use generic labels like "note", "text", or "content".

    Format your response EXACTLY like this, with no extra text:
    Summary: [Your summary here]
    Tags: [tag1, tag2, tag3]
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user",   "content": f"Note Content:\n{note_content}"}
        ],
        "temperature": 0.3
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GROQ_API_URL, json=payload, timeout=20.0, headers=headers
            )

        if response.status_code == 200:
            ai_text = response.json()["choices"][0]["message"]["content"].strip()
            summary, tags = "", []

            for line in ai_text.splitlines():
                line = line.strip()
                if line.lower().startswith("summary:"):
                    summary = line[len("summary:"):].strip()
                elif line.lower().startswith("tags:"):
                    raw = line[len("tags:"):].strip()
                    tags = [t.strip().lower() for t in raw.split(",") if t.strip()]

            await notes_collection.update_one(
                {"id": note_id},
                {"$set": {
                    "summary": summary or ai_text,
                    "tags":    tags if tags else ["indexed"]
                }}
            )
        else:
            await notes_collection.update_one(
                {"id": note_id},
                {"$set": {"summary": f"Groq error {response.status_code}", "tags": []}}
            )

    except Exception as e:
        await notes_collection.update_one(
            {"id": note_id},
            {"$set": {"summary": f"Error: {str(e)}", "tags": []}}
        )


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.post("/notes", response_model=NoteResponse, status_code=201)
async def create_note(incoming: NoteCreate, background_tasks: BackgroundTasks):
    note_id = await get_next_id()

    doc = {
        "id":      note_id,
        "title":   incoming.title,
        "content": incoming.content,
        "summary": "Thinking…",
        "tags":    []
    }

    await notes_collection.insert_one(doc)
    background_tasks.add_task(generate_ai_summary_and_tags, note_id, incoming.content)

    return clean(doc)


@app.get("/notes", response_model=List[NoteResponse])
async def get_all_notes():
    cursor = notes_collection.find({}, {"_id": 0}).sort("id", -1)
    return await cursor.to_list(length=None)


# NOTE: /notes/search must stay above /notes/{note_id} so FastAPI
# doesn't try to cast the string "search" as an integer.
@app.get("/notes/search", response_model=List[NoteResponse])
async def search_notes(q: str = ""):
    if not q.strip():
        return await get_all_notes()

    # Run the two queries separately — MongoDB won't mix $text and $regex in $or
    text_cursor = notes_collection.find(
        {"$text": {"$search": q}},
        {"_id": 0}
    )
    tag_cursor = notes_collection.find(
        {"tags": {"$regex": q, "$options": "i"}},
        {"_id": 0}
    )

    text_results = await text_cursor.to_list(length=None)
    tag_results  = await tag_cursor.to_list(length=None)

    # Merge and deduplicate by id
    seen = set()
    results = []
    for note in text_results + tag_results:
        if note["id"] not in seen:
            seen.add(note["id"])
            results.append(note)

    return results


@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    doc = await notes_collection.find_one({"id": note_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    return doc