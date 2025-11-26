# 🚀 Git_PR_Reviewer

An **AI-powered GitHub Pull Request Review System** built using **FastAPI, CrewAI, LangChain, and Groq LLM**.  
This project automatically analyzes PR diffs, detects issues, and generates structured, actionable code review feedback.

🔗 Repository: https://github.com/rahulmani-28/Git_PR_Reviewer

---

## 📌 What This Project Does

Git_PR_Reviewer is a backend system that:
- Fetches GitHub Pull Request diffs
- Analyzes code using AI agents
- Detects:
  - Logic issues
  - Code smells
  - Performance risks
  - Security vulnerabilities
  - Readability problems
- Generates **real developer-style PR review comments**
- Exposes everything via a **FastAPI REST API**

This can be used as:
- A **GitHub PR automation tool**
- A **developer assistant**
- A **startup MVP for automated code review**

---

## 🧠 Tech Stack

### ✅ Backend Framework
- **FastAPI** – High-performance Python API framework
- **Uvicorn** – ASGI server for FastAPI

### ✅ AI & Agents
- **CrewAI** – Multi-agent task orchestration
- **LangChain** – LLM chains, prompts, and reasoning
- **LangChain-Groq** – Groq LLM integration
- **Groq LLM API** – Ultra-fast inference engine

### ✅ GitHub Integration
- **PyGitHub** – GitHub REST API wrapper
- **GitHub Personal Access Token (PAT)** – Secure PR access

### ✅ Environment & Config
- **Python 3.11**
- **python-dotenv** – Environment variable management
- **.env config system**

### ✅ Developer Tooling
- **Git & GitHub**
- **PowerShell**
- **Virtual Environments (venv)**

---

## 🏗️ Project Structure

Git_PR_Reviewer/
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── pr_reviewer.py # PR parsing logic (future)
│ ├── agents/ # CrewAI agents
│ ├── services/ # GitHub & LLM services
│
├── .env # API keys (ignored)
├── .gitignore
├── README.md

yaml
Copy code

---

## ⚙️ Installation & Setup

### ✅ 1. Clone the Repository

git clone https://github.com/rahulmani-28/Git_PR_Reviewer.git
cd Git_PR_Reviewer

### ✅ 2. Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate

✅ 3. Install Dependencies
pip install fastapi uvicorn crewai langchain langchain-groq pygithub python-dotenv

✅ 4. Add Environment Variables

Create a .env file (DO NOT COMMIT IT):

GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_personal_access_token

Groq API Key: https://console.groq.com/keys
GitHub classic Token : GitHub Settings -> Developer Settings


▶️ Run the FastAPI Server
cd backend
python -m uvicorn main:app --reload

Open another terminal 
▶️ Run the Streamlit for frontend
cd backend
streamlit run frontend.py



