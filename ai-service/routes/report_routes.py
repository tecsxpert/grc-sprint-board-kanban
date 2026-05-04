from flask import Blueprint, jsonify, request, g
from services.groq_client import GroqClient
import os

report_bp = Blueprint("report", __name__)

# Initialize Groq client
groq_client = GroqClient()

def load_prompt(filename):
    """Load prompt template from file"""
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(prompt_path, 'r') as f:
        return f.read().strip()

@report_bp.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Report route working"})

@report_bp.route("/recommend", methods=["POST"])
def recommend():
    """AI-powered task recommendations for sprint planning"""
    try:
        data = getattr(g, 'sanitized_json', request.get_json())
        if not data or 'tasks' not in data:
            return jsonify({"error": "Missing 'tasks' field in request"}), 400

        tasks = data['tasks']
        prompt_template = load_prompt('recommend_prompt.txt')

        # Format tasks for the prompt
        tasks_text = "\n".join([f"- {task}" for task in tasks])
        full_prompt = f"{prompt_template}\n\nTASKS TO ANALYZE:\n{tasks_text}"

        recommendation = groq_client.generate_response(full_prompt)

        return jsonify({
            "recommendation": recommendation,
            "model": "llama-3.3-70b-versatile",
            "endpoint": "/recommend"
        })

    except Exception as e:
        return jsonify({"error": f"AI recommendation failed: {str(e)}"}), 500

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """AI-powered sprint report generation"""
    try:
        data = getattr(g, 'sanitized_json', request.get_json())
        if not data:
            return jsonify({"error": "Request body required"}), 400

        prompt_template = load_prompt('generate_report_prompt.txt')

        # Build context from request data
        context_parts = []
        if 'sprint_name' in data:
            context_parts.append(f"SPRINT: {data['sprint_name']}")
        if 'completed_tasks' in data and 'total_tasks' in data:
            completion_rate = (data['completed_tasks'] / data['total_tasks']) * 100
            context_parts.append(f"COMPLETION: {data['completed_tasks']}/{data['total_tasks']} tasks ({completion_rate:.1f}%)")
        if 'team_size' in data:
            context_parts.append(f"TEAM SIZE: {data['team_size']} members")
        if 'key_deliverables' in data:
            deliverables = "\n".join([f"- {d}" for d in data['key_deliverables']])
            context_parts.append(f"KEY DELIVERABLES:\n{deliverables}")

        context = "\n".join(context_parts)
        full_prompt = f"{prompt_template}\n\nSPRINT DATA:\n{context}"

        report = groq_client.generate_response(full_prompt)

        return jsonify({
            "report": report,
            "model": "llama-3.3-70b-versatile",
            "endpoint": "/generate-report"
        })

    except Exception as e:
        return jsonify({"error": f"Report generation failed: {str(e)}"}), 500

@report_bp.route("/describe", methods=["POST"])
def describe():
    """AI-powered task description generation"""
    try:
        data = getattr(g, 'sanitized_json', request.get_json())
        if not data or 'task_title' not in data:
            return jsonify({"error": "Missing 'task_title' field in request"}), 400

        task_title = data['task_title']
        prompt_template = load_prompt('describe_prompt.txt')

        # Build context from request data
        context_parts = [f"TASK TITLE: {task_title}"]
        if 'business_context' in data:
            context_parts.append(f"BUSINESS CONTEXT: {data['business_context']}")
        if 'current_state' in data:
            context_parts.append(f"CURRENT STATE: {data['current_state']}")
        if 'requirements' in data:
            reqs = "\n".join([f"- {r}" for r in data['requirements']])
            context_parts.append(f"REQUIREMENTS:\n{reqs}")

        context = "\n".join(context_parts)
        full_prompt = f"{prompt_template}\n\nTASK DETAILS:\n{context}"

        description = groq_client.generate_response(full_prompt)

        return jsonify({
            "description": description,
            "model": "llama-3.3-70b-versatile",
            "endpoint": "/describe"
        })

    except Exception as e:
        return jsonify({"error": f"Task description failed: {str(e)}"}), 500