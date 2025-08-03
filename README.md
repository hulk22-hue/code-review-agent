# Autonomous Code Review Agent

A fully autonomous, goal-oriented code review system that uses an AI agent (LLM) to analyze GitHub pull requests for code issues, best practices, bugs, and more.
Built with FastAPI, Celery, Redis, and Ollama (for local LLM inference).

---

## ⚡ Requirements

- Python 3.8+
- Ollama (local LLM server)
- Redis server
- Node.js (if you want to use Ollama's node client—optional)
- 4GB+ RAM minimum for most code LLMs

**Model RAM Requirements:**
- `phi3:mini`: requires at least 4GB free RAM (more is safer)
- `codellama:7b`: requires ~4GB RAM
- `llama3:8b`: requires at least 6GB free RAM (ideally 8GB+)
- If you get "model request too large" or OOM, use a smaller model!

---

## 🖥️ Step 1: Run Locally (Manual, or Script)

You can start everything in separate terminals/tmux panes OR use the provided script for Mac/Linux/WSL2.

---

### A. Manual Steps

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis**
   ```bash
   redis-server
   ```
   (Or, on Mac: `brew install redis` then `brew services start redis`)

3. **Start Ollama**
   ```bash
   ollama serve
   ```
   (First, [install Ollama](https://ollama.ai/).)

4. **Pull an LLM model (first time only)**
   ```bash
   ollama pull phi3:mini
   ```
   (Or use `codellama:7b` or another model—see RAM notes above.)

5. **Set up your `.env`**
   ```bash
   cp .env.example .env
   # Edit if needed, defaults are fine for public repos.
   # For local development, change URLs from redis:6379 and ollama:11434 to localhost:6379 and localhost:11434
    # The redis/ollama hostnames work for Docker, but use localhost for local development.
   ```

6. **Start Celery worker**
   ```bash
   celery -A app.celery_worker.celery worker --loglevel=INFO
   ```

7. **Start FastAPI app**
   ```bash
   uvicorn app.main:app --reload
   ```

---

### B. Automated Script

Create and run `run_local.sh` to launch all services in new terminals:

```bash
#!/bin/bash

# Simple runner for MacOS/Linux/WSL2.
# Starts Redis, Ollama, Celery, and FastAPI in separate terminal windows.

# Start Redis
osascript -e 'tell app "Terminal" to do script "redis-server"'
sleep 1

# Start Ollama
osascript -e 'tell app "Terminal" to do script "ollama serve"'
sleep 1

# Start Celery Worker
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && source venv/bin/activate && celery -A app.celery_worker.celery worker --loglevel=INFO"'
sleep 1

# Start FastAPI
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && source venv/bin/activate && uvicorn app.main:app --reload"'
```

Save this as `run_local.sh`, `chmod +x run_local.sh`, then run `./run_local.sh`.
- On Linux: Replace `osascript` blocks with your terminal's tab/spawn commands or use `tmux new-window ...`.
- On Windows: Start each manually or use Windows Terminal with tabs.

---

## 🐳 Step 2 (Optional): Docker Compose

If you prefer Docker Compose:

1. **Install Docker Desktop and start it.**
2. **Copy `.env.example` to `.env`**
   ```bash
   cp .env.example .env
   ```

3. **Start all services:**
   ```bash
   docker-compose up --build
   ```

4. **Pull the model in Ollama container (first time only):**
   ```bash
   docker exec -it ollama ollama pull phi3:mini
   ```
   (Use `codellama:7b` or `llama3:8b` only if your system has sufficient RAM!)

---

## 🚀 How to Use

---

### Analyze a Pull Request

1. **Send a PR analysis request:**
   ```bash
   curl -X POST http://localhost:8000/analyze-pr \
   -H 'Content-Type: application/json' \
   -d '{"repo_url": "https://github.com/tiangolo/fastapi", "pr_number": 11620}'
   ```

2. **Get the returned `task_id`**
3. **Check task status:**
   ```bash
   curl http://localhost:8000/status/<task_id>
   ```

4. **Fetch results when status is "completed":**
   ```bash
   curl http://localhost:8000/results/<task_id>
   ```

---

## ⚠️ Model/RAM Notes

- `phi3:mini`: needs 4GB+ RAM
- `codellama:7b`: needs 4GB+ RAM
- `llama3:8b`: needs 6GB+ RAM
- If you see "model request too large for system," your RAM is insufficient—use a smaller model or a bigger machine.
- On Docker, ensure your Docker Desktop memory allocation matches the requirement!

---

## 📄 License

MIT