from pathlib import Path

from flask import Blueprint, g, request

from services.groq_client import GroqClient
from utils.logging_config import get_logger
from utils.responses import api_response

report_bp = Blueprint("report", __name__)
logger = get_logger(__name__)
PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    return (PROMPT_DIR / filename).read_text(encoding="utf-8").strip()


def request_json():
    return getattr(g, "sanitized_json", None) or request.get_json(silent=True) or {}


def groq_content(result: dict) -> tuple[dict, str, int]:
    if result.get("success"):
        return {"content": result["data"]["content"], "model": result["data"]["model"]}, "AI response generated", 200
    return {"is_fallback": True}, result.get("message", "AI service temporarily unavailable"), 503


@report_bp.get("/health")
def health():
    return api_response(True, {"status": "healthy"}, "AI service running")


@report_bp.get("/status")
def status():
    return api_response(True, {"status": "operational"}, "AI service operational")


@report_bp.post("/describe")
def describe():
    data = request_json()
    task_title = data.get("task_title")
    if not isinstance(task_title, str) or not task_title.strip():
        return api_response(False, message="task_title is required", status_code=400)

    prompt = load_prompt("describe_prompt.txt").format(
        task_title=task_title,
        business_context=data.get("business_context", "Not provided"),
        current_state=data.get("current_state", "Not provided"),
        requirements="\n".join(f"- {item}" for item in data.get("requirements", [])) or "Not provided",
    )
    payload, message, status_code = groq_content(GroqClient().generate_response(prompt, temperature=0.25))
    return api_response(status_code == 200, {"description": payload}, message, status_code)


@report_bp.post("/recommend")
def recommend():
    data = request_json()
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return api_response(False, message="tasks must be a non-empty list", status_code=400)

    prompt = load_prompt("recommend_prompt.txt").format(
        tasks="\n".join(f"- {task}" for task in tasks),
        sprint_goal=data.get("sprint_goal", "Not provided"),
        team_capacity=data.get("team_capacity", "Not provided"),
    )
    payload, message, status_code = groq_content(GroqClient().generate_response(prompt, temperature=0.2))
    return api_response(status_code == 200, {"recommendation": payload}, message, status_code)


@report_bp.post("/generate-report")
def generate_report():
    data = request_json()
    sprint_name = data.get("sprint_name")
    if not isinstance(sprint_name, str) or not sprint_name.strip():
        return api_response(False, message="sprint_name is required", status_code=400)

    total_tasks = int(data.get("total_tasks", 0) or 0)
    completed_tasks = int(data.get("completed_tasks", 0) or 0)
    if total_tasks < 0 or completed_tasks < 0 or completed_tasks > max(total_tasks, 0):
        return api_response(False, message="task counts are invalid", status_code=400)

    prompt = load_prompt("generate_report_prompt.txt").format(
        sprint_name=sprint_name,
        completed_tasks=completed_tasks,
        total_tasks=total_tasks,
        blockers="\n".join(f"- {item}" for item in data.get("blockers", [])) or "None reported",
        key_deliverables="\n".join(f"- {item}" for item in data.get("key_deliverables", [])) or "Not provided",
    )
    payload, message, status_code = groq_content(GroqClient().generate_response(prompt, temperature=0.25, max_tokens=900))
    return api_response(status_code == 200, {"report": payload}, message, status_code)
