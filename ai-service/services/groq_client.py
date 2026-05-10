import os
from typing import Any

import requests
from dotenv import load_dotenv

try:
    from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
except ImportError:
    def retry(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

    def retry_if_exception_type(*args, **kwargs):
        return None

    def stop_after_attempt(*args, **kwargs):
        return None

    def wait_exponential(*args, **kwargs):
        return None

from utils.logging_config import get_logger
from utils.responses import fallback_payload

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
logger = get_logger(__name__)


class GroqClient:
    def __init__(self, api_key: str | None = None, model: str | None = None, timeout: int | None = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or os.getenv("GROQ_MODEL", DEFAULT_MODEL)
        self.timeout = timeout or int(os.getenv("GROQ_TIMEOUT_SECONDS", "20"))

    def generate_response(self, prompt: str, *, temperature: float = 0.3, max_tokens: int = 700) -> dict[str, Any]:
        if not self.api_key:
            logger.warning("groq_api_key_missing")
            return fallback_payload()

        try:
            response = self._post_completion(prompt, temperature, max_tokens)
            content = self._extract_content(response)
            return {
                "success": True,
                "is_fallback": False,
                "message": "AI response generated",
                "data": {
                    "content": content,
                    "model": self.model,
                },
            }
        except Exception as exc:
            logger.error("groq_request_failed", error=str(exc))
            return fallback_payload()

    @retry(
        retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError, requests.HTTPError, ValueError)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def _post_completion(self, prompt: str, temperature: float, max_tokens: int) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a concise sprint-board assistant. Use only the supplied project context.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _extract_content(response_json: dict[str, Any]) -> str:
        try:
            content = response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Unexpected Groq response format") from exc

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Empty Groq response content")
        return content.strip()
