from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.utils.logging import configure_logging

configure_logging
app = FastAPI(title="Autonomous Code Review Agent")

app.include_router(api_router)

@app.get("/")
def health():
    return {"status": "ok"}