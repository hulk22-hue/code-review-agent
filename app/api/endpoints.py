from fastapi import APIRouter, HTTPException
from app.api.schemas import AnalyzePRRequest, AnalyzePRResponse
from app.services.task_service import (
    launch_code_review_task,
    get_task_status,
    get_task_results,
)

router = APIRouter()

@router.post("/analyze-pr", response_model=AnalyzePRResponse)
def analyze_pr(request: AnalyzePRRequest):
    task_id = launch_code_review_task(request)
    return AnalyzePRResponse(task_id=task_id)

@router.get("/status/{task_id}")
def status(task_id: str):
    status = get_task_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": status}

@router.get("/results/{task_id}")
def results(task_id: str):
    result = get_task_results(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return result