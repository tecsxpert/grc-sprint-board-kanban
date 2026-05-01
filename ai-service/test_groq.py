from services.groq_client import GroqClient

def main():
    try:
        # Initialize client
        client = GroqClient()

        # Test prompt
        response = client.generate_response(
            "Summarize a sprint where 8 out of 10 tasks are completed in one sentence"
        )

        print(" AI Output:")
        print(response)

    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()