from flask import jsonify


def api_response(success, data=None, message="", status_code=200):
    payload = {
        "success": bool(success),
        "data": data or {},
        "message": message,
    }
    return jsonify(payload), status_code


def fallback_payload(message="AI service temporarily unavailable"):
    return {
        "success": False,
        "is_fallback": True,
        "message": message,
    }
