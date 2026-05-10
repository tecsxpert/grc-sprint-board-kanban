from dotenv import load_dotenv

from services.groq_client import GroqClient


def main():
    load_dotenv()
    client = GroqClient()
    result = client.generate_response("Reply with one short sprint planning tip.")

    if result.get("success"):
        print("Groq API connection successful")
        print(result["data"]["content"])
        return

    print("Groq API test failed cleanly")
    print(result["message"])


if __name__ == "__main__":
    main()
