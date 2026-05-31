# 🚀 Smart Notes API

A modern, fast, and asynchronous Python backend built with **FastAPI**. This application maps classic CRUD principles over from the MERN stack and leverages a local **Ollama** LLM instance via background tasks to automatically summarize notes and generate contextual tags.

---

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Server Runner:** Uvicorn (ASGI)
* **Data Validation:** Pydantic
* **HTTP Client:** HTTPX (for non-blocking AI API calls)
* **AI Layer:** Local Ollama instance (Running `llama3`)

---

## 📂 Project Architecture
```text
smart-notes/            # Root Git repository
├── backend/            # FastAPI application
│   ├── main.py         # App entry point, schemas, and routes
│   ├── requirements.txt# Python package dependencies
│   └── venv/           # Isolated virtual environment (ignored by Git)
└── .gitignore          # Git exclusion rules

```

---

## 🚀 Getting Started (Backend Setup)

Follow these steps to get your local development environment up and running.

### 1. Navigate to the Backend Folder

Open your terminal, ensure you are in the project root directory, and move into the backend subdirectory:

```bash
cd backend

```

### 2. Create and Activate the Virtual Environment

Isolate your Python dependencies locally (similar to standard `node_modules` scoping):

```bash
# Create the environment
python3 -m venv venv

# Activate the environment (macOS/Linux)
source venv/bin/activate

```

*Note: Your terminal prompt should now be prefixed with `(venv)`.*

### 3. Install Dependencies

Install all the required Python packages specified in the requirements file:

```bash
pip install -r requirements.txt

```

### 4. Start the Development Server

Launch the application using Uvicorn with hot-reloading enabled (similar to `nodemon` in Node.js):

```bash
uvicorn main:app --reload

```

The server will boot up locally at **`http://127.0.0.1:8000`**.

---

## 🦙 Setting up the AI Layer (Ollama)

To prevent connection timeout errors and allow your background tasks to process text successfully, ensure Ollama is correctly running on your machine:

1. **Launch the Ollama App:** Ensure the Ollama application is active in your macOS menu bar.
2. **Pull the Model:** Open a separate terminal window and verify you have the correct model downloaded locally:
```bash
ollama run llama3

```


3. **Verify Connection:** Open your browser and navigate to `http://localhost:11434/`. You should see the message: `"Ollama is running"`.

---

## 🔌 API Testing & Interactive Documentation

FastAPI automatically evaluates your code routers and schemas to generate self-documenting interactive environments. Once your server is running, you can open the following links in your browser to test your endpoints:

* **Swagger UI Docs:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs) *(Recommended for executing manual POST and GET requests directly from the browser)*
* **ReDoc UI Docs:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)