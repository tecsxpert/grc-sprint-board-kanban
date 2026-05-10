import re
import unicodedata

from flask import g, request

from utils.responses import api_response
from utils.logging_config import get_logger

try:
    import bleach
except ImportError:
    bleach = None

logger = get_logger(__name__)

MAX_CONTENT_LENGTH = 16 * 1024
MAX_STRING_LENGTH = 4000
MAX_NESTING_DEPTH = 6

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard previous instructions",
    "system prompt",
    "reveal secrets",
    "bypass rules",
    "bypass safety",
    "jailbreak",
    "developer message",
    "hidden instructions",
]

DANGEROUS_PATTERNS = [
    r"<\s*script",
    r"javascript\s*:",
    r"\b(drop|delete|truncate)\s+table\b",
    r"\bunion\s+select\b",
    r"'\s*or\s*'1'\s*=\s*'1",
]


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", value)
    return value.strip()


def sanitize_input(value: str) -> str:
    normalized = normalize_text(value)
    if bleach:
        return bleach.clean(normalized, tags=[], attributes={}, strip=True)
    return re.sub(r"<[^>]*>", "", normalized)


def detect_prompt_injection(value: str) -> bool:
    compact = re.sub(r"[\s_\-.:;]+", " ", normalize_text(value).lower())
    squashed = re.sub(r"[^a-z0-9]+", "", compact)
    for pattern in PROMPT_INJECTION_PATTERNS:
        pattern_squashed = re.sub(r"[^a-z0-9]+", "", pattern.lower())
        if pattern in compact or pattern_squashed in squashed:
            return True
    return False


def detect_dangerous_content(value: str) -> bool:
    normalized = normalize_text(value).lower()
    return any(re.search(pattern, normalized, re.IGNORECASE) for pattern in DANGEROUS_PATTERNS)


def sanitize_json(value, depth=0):
    if depth > MAX_NESTING_DEPTH:
        raise ValueError("JSON nesting depth exceeded")
    if isinstance(value, dict):
        return {str(key): sanitize_json(item, depth + 1) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_json(item, depth + 1) for item in value]
    if isinstance(value, str):
        if len(value) > MAX_STRING_LENGTH:
            raise ValueError("Input too long")
        if detect_prompt_injection(value) or detect_dangerous_content(value):
            raise ValueError("Invalid input")
        return sanitize_input(value)
    return value


def security_middleware():
    if request.content_length and request.content_length > MAX_CONTENT_LENGTH:
        logger.warning("request_too_large", path=request.path, remote_addr=request.remote_addr)
        return api_response(False, message="Request body too large", status_code=400)

    if request.method not in {"POST", "PUT", "PATCH"}:
        return None

    if not request.is_json:
        return api_response(False, message="Content-Type must be application/json", status_code=400)

    data = request.get_json(silent=True)
    if not data:
        return api_response(False, message="Request JSON body is required", status_code=400)

    try:
        g.sanitized_json = sanitize_json(data)
    except ValueError as exc:
        logger.warning("input_rejected", reason=str(exc), path=request.path, remote_addr=request.remote_addr)
        return api_response(False, message=str(exc), status_code=400)

    return None
