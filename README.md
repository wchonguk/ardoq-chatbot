# 🤖 Ardoq Chatbot (Flask App)

A lightweight chatbot built with Python and Flask that lets users interact with the Ardoq API using natural language commands. It supports querying workspaces, components, and more — with responses formatted in a chat-friendly way.

---

## 🔧 Features

- ✅ Conversational chat interface (HTML + JS frontend)
- ✅ Query Ardoq workspaces and components via REST API
- ✅ Natural language command parser with basic intent routing
- ✅ Summarized responses (Claude-style) rather than raw JSON
- ✅ Secure token management using `.env` file
- ✅ Low-maintenance and free to run locally or on cloud (Render, PythonAnywhere)

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ardoq-chatbot.git
cd ardoq-chatbot

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

### 3. Install dependencies

```bash
pip install -r requirements.txt

### 4. Add your .env file (⚠️ Do NOT commit this)
Create a .env file in the project root:

```bash
ARDOQ_API_TOKEN=your-token-here

Make sure .env is listed in .gitignore so it won’t be pushed to GitHub.

### 5. Add your .env file (⚠️ Do NOT commit this)

```bash
flask run

Then open your browser to http://localhost:5000
