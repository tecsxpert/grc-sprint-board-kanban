import re
from flask import request, jsonify

# Common prompt injection patterns
SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "act as",
    "system prompt",
    "bypass",
    "jailbreak"
]


def sanitize_input(text):
    # Remove HTML tags
    clean_text = re.sub(r'<.*?>', '', text)

    # Trim spaces
    clean_text = clean_text.strip()

    return clean_text


def detect_prompt_injection(text):
    text_lower = text.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in text_lower:
            return True

    return False


def security_middleware():
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid request body"}), 400

        for key, value in data.items():
            if isinstance(value, str):

                # Length check
                if len(value) > 500:
                    return jsonify({"error": "Input too long"}), 400

                # Prompt injection detection
                if detect_prompt_injection(value):
                    return jsonify({"error": "Suspicious input detected"}), 400

                # Sanitize input
                data[key] = sanitize_input(value)

        request.json = data  # overwrite sanitized data