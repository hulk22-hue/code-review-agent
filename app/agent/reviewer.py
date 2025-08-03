import httpx
from app.utils.config import OLLAMA_BASE_URL
import json
import logging

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
You are an expert code reviewer. Given the following file diff from a GitHub PR, review for:
- Code style and formatting issues
- Potential bugs or errors
- Performance improvements
- Best practices

Output structured JSON as:
[
  {{
    "type": "...",
    "line": ...,
    "description": "...",
    "suggestion": "..."
  }},
  ...
]
File: {filename}
Diff:
{diff}
Only output a valid JSON array. Do not include any additional text or formatting.
"""

def analyze_code_files(files):
    results = []
    for f in files:
        prompt = PROMPT_TEMPLATE.format(filename=f["name"], diff=f["patch"])
        try:
            response = httpx.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": "phi3:mini", "prompt": prompt, "stream": False},
                timeout=90
            )
            response.raise_for_status()
            text = response.json()["response"]
            logger.info(f"\n[DEBUG] LLM raw output for {f['name']}:\n{text}\n")
            try:
                issues = json.loads(text)
            except Exception as e:
                logger.error(f"[DEBUG] Failed to parse JSON for {f['name']}: {e}")
                issues = []
            results.append({
                "name": f["name"],
                "issues": issues
            })
        except Exception as err:
            logger.error(f"[DEBUG] Error analyzing {f['name']}: {err}")
            results.append({
                "name": f["name"],
                "issues": [],
                "error": str(err)
            })
    return results