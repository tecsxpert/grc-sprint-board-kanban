from services.groq_client import GroqClient


PROMPTS = [
    "Describe a task to add board filtering.",
    "Describe a task to add Redis rate limiting.",
    "Describe a task to add Docker health checks.",
    "Recommend priorities for three blocked tasks.",
    "Recommend priorities for a low-capacity sprint.",
    "Recommend testing work before demo.",
    "Report a sprint with 8 of 10 tasks done.",
    "Report a sprint with two blockers.",
    "Report a security cleanup sprint.",
    "Report final demo readiness.",
]


def score_output(text: str) -> dict:
    return {
        "has_content": bool(text.strip()),
        "has_structure": any(marker in text.lower() for marker in ["summary", "risks", "next", "criteria"]),
        "hallucination_flag": "as an ai" in text.lower(),
    }


def main():
    client = GroqClient()
    for prompt in PROMPTS:
        result = client.generate_response(prompt)
        content = result.get("data", {}).get("content", "")
        print({"prompt": prompt, "success": result.get("success"), "score": score_output(content)})


if __name__ == "__main__":
    main()
