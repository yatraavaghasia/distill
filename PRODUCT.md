# Distill — Product Document

## One-liner
*You think. Distill remembers.*

## The problem
The notes app market has two ends, both broken.

**Dumb-fast** — Apple Notes, Google Keep. Zero friction to capture, but nothing
happens to your notes after. They pile up. You never find them again.

**Intelligent-but-heavy** — Notion, Obsidian, Roam. Powerful, but they demand
upfront structure. You have to decide where a note lives, what tags it gets, how
it connects to everything else. Most people abandon these systems within a month
because maintaining them becomes a second job.

## The gap Distill fills
Distill sits exactly between those two ends.

> You write freely. It organises automatically.

No folders. No manual tags. No deciding where things go. You write, the AI
thinks, you search. That is the entire loop.

```
Capture without friction  →  AI extracts meaning  →  Find anything later
```

## USP
A personal knowledge archive that requires nothing from you except writing.
Every note is automatically summarised and tagged the moment you save it. Search
works across meaning, not just exact words — so you can search "mortality" and
find a note you wrote about a Macbeth quote even if you never used that word.

## Use cases

**Researchers and students**
Read heavily, want to retain what they've read. Paste a passage or write a
reflection, Distill summarises and tags it. Six months later, search a theme and
find everything you ever captured on it.

**Writers and journalists**
Collect observations, fragments, overheard lines, half-formed ideas. The problem
for writers isn't capturing — it's finding things again when they're relevant.
Distill's search across summaries means you're searching the meaning of a note,
not just its exact words.

**Professionals**
Come out of meetings, articles, conversations with insights they want to keep but
no time to file. Quick capture, AI handles the rest.

**Curious people who read a lot**
The Commonplace Book use case. People into philosophy, history, science who want
a private running archive of things that struck them. Distill is a digital
commonplace book with an AI librarian.

## What it is not
- Not a project management tool
- Not a collaborative workspace
- Not a replacement for Notion
- Not trying to be everything

It is a personal thinking archive. Smaller audience, much more loyal.

## Positioning
| | Capture speed | Auto-organisation | Search depth |
|---|---|---|---|
| Apple Notes | ✅ Fast | ❌ None | ❌ Exact words only |
| Notion | 🟡 Slow | ❌ Manual | 🟡 Exact words |
| Distill | ✅ Fast | ✅ Automatic | ✅ Meaning-based |

## Taglines
- *You think. Distill remembers.*
- *Write anything. Find everything.*
- *Your thinking, archived automatically.*
- *The notes app that does the filing for you.*

## Tech stack
- **Frontend** — Vanilla HTML/CSS/JS, single file, no framework
- **Backend** — FastAPI (Python), async
- **AI** — Groq API (llama-3.3-70b-versatile) for summarisation and tagging
- **Database** — MongoDB Atlas (cloud-hosted, persistent)
- **Deployment** — Vercel (frontend) + Railway (backend)

## The one-paragraph pitch
Most people who try to keep notes seriously eventually give up — not because
they stop having ideas, but because every system they try demands too much
maintenance. Distill removes that entirely. You write the way you already do,
and the AI handles everything that usually requires discipline: summarising what
you wrote, deciding what it's about, making it findable later. It's the notes
app for people who have already tried five notes apps.