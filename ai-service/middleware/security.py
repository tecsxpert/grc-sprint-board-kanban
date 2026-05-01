import re
from flask import request, jsonify
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Common prompt injection patterns (CWE-95)
SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "act as",
    "system prompt",
    "bypass",
    "jailbreak",
    "override",
    "forget the",
    "disregard",
    "counter-instruction"
]


def sanitize_input(text):
    """Sanitize input by removing dangerous content"""
    # Remove HTML tags (XSS prevention)
    clean_text = re.sub(r'<.*?>', '', text)
    
    # Remove script tags explicitly
    clean_text = re.sub(r'script|javascript:', '', clean_text, flags=re.IGNORECASE)
    
    # Trim spaces
    clean_text = clean_text.strip()

    return clean_text


def detect_prompt_injection(text):
    """Detect prompt injection attempts"""
    text_lower = text.lower()
    
    # Remove common obfuscation (spaces, newlines, special chars)
    text_normalized = re.sub(r'[\s\n\r\t_\-]', '', text_lower)

    for pattern in SUSPICIOUS_PATTERNS:
        pattern_normalized = re.sub(r'[\s\n\r\t_\-]', '', pattern)
        if pattern_normalized in text_normalized:
            return True

    return False


def sanitize_error(message, show_details=False):
    """Sanitize error messages (CRT-004 fix)"""
    if show_details:
        return message  # Server-side logging only
    
    # Return generic error to client
    return "Processing failed"


def security_middleware():
    """
    Central security middleware (CRT-002, CRT-004 improvements)
    Validates all incoming requests
    """
    # Skip security checks for GET requests on health endpoints
    if request.path in ['/health', '/status'] and request.method == 'GET':
        return None
    
    # Only validate POST/PUT/PATCH requests
    if request.method not in ["POST", "PUT", "PATCH"]:
        return None
    
    # Check for valid JSON
    if not request.is_json:
        logger.warning(f"Invalid content-type from {request.remote_addr}: {request.content_type}")
        return jsonify({"error": "Invalid request"}), 400
    
    data = request.get_json(silent=True)

    if not data:
        logger.warning(f"Empty request body from {request.remote_addr}")
        return jsonify({"error": "Invalid request"}), 400

    # Validate each field (CRT-005 improvement)
    for key, value in data.items():
        if isinstance(value, str):
            # Length check (CWE-400 prevention)
            if len(value) > 500:
                logger.warning(f"Oversized input from {request.remote_addr}: {len(value)} chars")
                return jsonify({"error": "Input too long"}), 400

            # Prompt injection detection (CWE-95)
            if detect_prompt_injection(value):
                logger.warning(f"Prompt injection attempt from {request.remote_addr}")
                return jsonify({"error": "Invalid input"}), 400

            # Sanitize input
            data[key] = sanitize_input(value)
        elif isinstance(value, dict):
            # Check nesting depth (CRT-005 fix)
            if _check_nesting_depth(value) > 5:
                logger.warning(f"Excessive JSON nesting from {request.remote_addr}")
                return jsonify({"error": "Invalid request structure"}), 400

    request.json = data  # Overwrite with sanitized data
    return None


def _check_nesting_depth(obj, current_depth=0, max_depth=10):
    """Check JSON nesting depth (CRT-005 DoS prevention)"""
    if current_depth > max_depth:
        return current_depth
    
    if isinstance(obj, dict):
        if not obj:
            return current_depth
        return max(_check_nesting_depth(v, current_depth + 1) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return current_depth
        return max(_check_nesting_depth(item, current_depth + 1) for item in obj)
    else:
        return current_depth