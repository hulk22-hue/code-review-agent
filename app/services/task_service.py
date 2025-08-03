# app/services/task_service.py

from app.celery_worker import celery
from app.github_tools.github_client import fetch_pr_files_and_diffs
from app.agent.reviewer import analyze_code_files
import redis
import json
from app.utils.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def launch_code_review_task(request):
    result = analyze_pr_task.delay(request.repo_url, request.pr_number, request.github_token)
    r.set(f"task:{result.id}:status", "pending")
    return result.id

def get_task_status(task_id):
    status = r.get(f"task:{task_id}:status")
    return status.decode() if status else None

def get_task_results(task_id):
    data = r.get(f"task:{task_id}:result")
    status = r.get(f"task:{task_id}:status")
    if not data or not status:
        return None
    result = json.loads(data)
    return {
        "task_id": task_id,
        "status": status.decode(),
        "results": result
    }

@celery.task(bind=True)
def analyze_pr_task(self, repo_url, pr_number, github_token=None):
    task_id = self.request.id
    try:
        r.set(f"task:{task_id}:status", "processing")
        files = fetch_pr_files_and_diffs(repo_url, pr_number, github_token)
        results = analyze_code_files(files)
        summary = {
            "files": results,
            "summary": {
                "total_files": len(results),
                "total_issues": sum(len(f["issues"]) for f in results),
                "critical_issues": sum(1 for f in results for i in f["issues"] if i["type"] == "bug")
            }
        }
        r.set(f"task:{task_id}:status", "completed")
        r.set(f"task:{task_id}:result", json.dumps(summary))
        return summary
    except Exception as e:
        r.set(f"task:{task_id}:status", "failed")
        r.set(f"task:{task_id}:result", json.dumps({"error": str(e)}))
        raise