import json
import os
import urllib.error
import urllib.request

OAUTH2_ACCESS_TOKEN = os.environ["GROQ_API_KEY"]

API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are a recipe optimization agent.
The user will provide ONLY a dish name (e.g. "lasagna", "kanafeh", "chicken curry").
Your job:
1. Think of common real-world versions of this dish.
2. Identify typical ingredients and preparation methods.
3. Create a simplified version that is:
   - high in protein
   - low in calories
   - easy to prepare
   - minimal ingredients
4. Do NOT ask the user for ingredients.
5. Always assume the dish is a general concept, not a fixed recipe.
"""


def call_llm(user_message):
    request = urllib.request.Request(
        API_URL,
        data=json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
        }).encode(),
        headers={
            "Authorization": f"Bearer {OAUTH2_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "recipe-agent/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as http_response:
            response = json.load(http_response)
    except urllib.error.HTTPError as error:
        print("ERROR:", error.read().decode())
        raise

    return response["choices"][0]["message"]["content"]


def main():
    print("🍳 Recipe Agent is ready!")
    print("Type dish name or 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Bye 👋")
            break

        answer = call_llm(user_input)
        print("\nAgent:\n", answer, "\n")


if __name__ == "__main__":
    main()