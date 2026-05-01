import os
import time
import requests
import dot0env

dotenv.load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqClient:

    def __init__(self):
        if not API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_response(self, prompt, retries=3):
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        for attempt in range(retries):
            try:
                response = requests.post(URL, headers=self.headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()

                else:
                    print(f" Error {response.status_code}: {response.text}")

            except Exception as e:
                print(f" Attempt {attempt+1} failed:", str(e))

            # Retry with exponential backoff
            if attempt < retries - 1:
                time.sleep(2 ** attempt)

        return "AI service unavailable"