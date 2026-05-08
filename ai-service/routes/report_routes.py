from flask import Blueprint, jsonify, request, g
from services.groq_client import GroqClient
from services.cache_service import (
    get_cached_response,
    set_cached_response
)

from datetime import datetime
import os

report_bp = Blueprint("report", __name__)

groq_client = GroqClient()


def load_prompt(filename):
    """Load prompt template from file"""

    prompt_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'prompts',
        filename
    )

    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


@report_bp.route("/test", methods=["GET"])
def test_route():

    return jsonify({
        "message": "Report route working"
    })


# =========================================================
# RECOMMEND
# =========================================================

@report_bp.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = getattr(g, 'sanitized_json', request.get_json())

        if not data or 'tasks' not in data:
            return jsonify({
                "error": "Missing 'tasks' field"
            }), 400

        tasks = data['tasks']

        prompt_template = load_prompt('recommend_prompt.txt')

        tasks_text = "\n".join([
            f"- {task}" for task in tasks
        ])

        full_prompt = f"""
{prompt_template}

TASKS TO ANALYZE:
{tasks_text}

IMPORTANT:
Return ONLY valid JSON in this exact format:

[
  {{
    "action_type": "TASK",
    "description": "Example",
    "priority": "HIGH"
  }}
]
"""

        # =========================
        # CACHE CHECK
        # =========================

        cached_response = get_cached_response(
            full_prompt,
            namespace="recommend"
        )

        if cached_response:

            return jsonify({
                "recommendations": cached_response,
                "cached": True,
                "endpoint": "/recommend",
                "generated_at": datetime.utcnow().isoformat()
            })

        # =========================
        # GROQ CALL
        # =========================

        recommendation = groq_client.generate_response(full_prompt)

        set_cached_response(
            full_prompt,
            recommendation,
            namespace="recommend"
        )

        return jsonify({
            "recommendations": recommendation,
            "cached": False,
            "model": "llama-3.3-70b-versatile",
            "endpoint": "/recommend",
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception:

        return jsonify({
            "recommendations": [
                {
                    "action_type": "FALLBACK",
                    "description": "AI service temporarily unavailable",
                    "priority": "LOW"
                }
            ],
            "is_fallback": True,
            "endpoint": "/recommend"
        }), 200


# =========================================================
# GENERATE REPORT
# =========================================================

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    try:

        data = getattr(g, 'sanitized_json', request.get_json())

        if not data:
            return jsonify({
                "error": "Request body required"
            }), 400

        prompt_template = load_prompt(
            'generate_report_prompt.txt'
        )

        context_parts = []

        if 'sprint_name' in data:
            context_parts.append(
                f"SPRINT: {data['sprint_name']}"
            )

        if 'completed_tasks' in data and 'total_tasks' in data:

            completion_rate = (
                data['completed_tasks'] /
                data['total_tasks']
            ) * 100

            context_parts.append(
                f"COMPLETION: "
                f"{data['completed_tasks']}/"
                f"{data['total_tasks']} "
                f"({completion_rate:.1f}%)"
            )

        if 'team_size' in data:
            context_parts.append(
                f"TEAM SIZE: {data['team_size']}"
            )

        if 'key_deliverables' in data:

            deliverables = "\n".join([
                f"- {d}" for d in data['key_deliverables']
            ])

            context_parts.append(
                f"KEY DELIVERABLES:\n{deliverables}"
            )

        context = "\n".join(context_parts)

        full_prompt = f"""
{prompt_template}

SPRINT DATA:
{context}

IMPORTANT:
Return structured report output.
"""

        # =========================
        # CACHE
        # =========================

        cached_response = get_cached_response(
            full_prompt,
            namespace="generate-report"
        )

        if cached_response:

            return jsonify({
                "report": cached_response,
                "cached": True,
                "endpoint": "/generate-report",
                "generated_at": datetime.utcnow().isoformat()
            })

        # =========================
        # AI CALL
        # =========================

        report = groq_client.generate_response(full_prompt)

        set_cached_response(
            full_prompt,
            report,
            namespace="generate-report"
        )

        return jsonify({
            "report": report,
            "cached": False,
            "model": "llama-3.3-70b-versatile",
            "endpoint": "/generate-report",
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception:

        return jsonify({
            "report": "Fallback sprint report generated",
            "is_fallback": True,
            "endpoint": "/generate-report"
        }), 200


# =========================================================
# DESCRIBE
# =========================================================

@report_bp.route("/describe", methods=["POST"])
def describe():

    try:

        data = getattr(g, 'sanitized_json', request.get_json())

        if not data or 'task_title' not in data:

            return jsonify({
                "error": "Missing 'task_title' field"
            }), 400

        task_title = data['task_title']

        prompt_template = load_prompt(
            'describe_prompt.txt'
        )

        context_parts = [
            f"TASK TITLE: {task_title}"
        ]

        if 'business_context' in data:
            context_parts.append(
                f"BUSINESS CONTEXT: "
                f"{data['business_context']}"
            )

        if 'current_state' in data:
            context_parts.append(
                f"CURRENT STATE: "
                f"{data['current_state']}"
            )

        if 'requirements' in data:

            reqs = "\n".join([
                f"- {r}" for r in data['requirements']
            ])

            context_parts.append(
                f"REQUIREMENTS:\n{reqs}"
            )

        context = "\n".join(context_parts)

        full_prompt = f"""
{prompt_template}

TASK DETAILS:
{context}
"""

        # =========================
        # CACHE
        # =========================

        cached_response = get_cached_response(
            full_prompt,
            namespace="describe"
        )

        if cached_response:

            return jsonify({
                "description": cached_response,
                "cached": True,
                "endpoint": "/describe",
                "generated_at": datetime.utcnow().isoformat()
            })

        # =========================
        # AI CALL
        # =========================

        description = groq_client.generate_response(
            full_prompt
        )

        set_cached_response(
            full_prompt,
            description,
            namespace="describe"
        )

        return jsonify({
            "description": description,
            "cached": False,
            "model": "llama-3.3-70b-versatile",
            "endpoint": "/describe",
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception:

        return jsonify({
            "description": "Fallback task description generated",
            "is_fallback": True,
            "endpoint": "/describe"
        }), 200