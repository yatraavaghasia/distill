# Distill

> *You think. Distill remembers.*

A personal knowledge archive that requires nothing from you except writing.
Capture a note in seconds — the AI summarises it, tags it, and makes it
searchable by meaning, not just exact words.

## What it does

- **Write freely** — no folders, no manual tags, no upfront structure
- **AI summarises automatically** — every note gets a one-sentence distillation
  in the background via Groq
- **Search by meaning** — find notes by theme or tag, even if you never used
  that word when you wrote them

## Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML/CSS/JS |
| Backend | FastAPI + Python |
| AI | Groq API (llama-3.3-70b) |
| Database | MongoDB Atlas |
| Deploy | Vercel + Railway |

## Running locally

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/distill.git
cd distill
```

**2. Set up the backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Add your credentials**
```bash
cp .env.example .env
# then edit .env and fill in your values
```

**4. Start the server**
```bash
uvicorn main:app --reload
```

**5. Open the frontend**
```bash
cd ..
open index.html
```

## Environment variables

| Variable | Description |
|---|---|
| `MONGO_URI` | MongoDB Atlas connection string |
| `GROQ_API_KEY` | Groq API key (in main.py) |

## Live

| | URL |
|---|---|
| Frontend | https://distill-sigma.vercel.app |
| Backend | https://distill-production-5346.up.railway.app |

## Deploying

- **Frontend** → Vercel (import repo, zero config)
- **Backend** → Railway (set `MONGO_URI` env var, start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`)

See [PRODUCT.md](./PRODUCT.md) for the full product thinking behind Distill.