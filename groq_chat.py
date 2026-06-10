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
2. Create ONE optimized recipe that is:
   - high in protein
   - low in calories
   - easy to prepare
   - minimal ingredients

OUTPUT FORMAT (must follow exactly):

1. FULL RECIPE
- Name
- Ingredients
- Steps

2. NUTRITIONAL INFORMATION
- Protein (estimate in grams)
- Calories (estimate)
- Fat (estimate)
- Carbs (estimate)

3. SCORES (1–10)
- Protein score
- Calories score (lower calories = higher score)
- Ease of preparation score
- Overall score (weighted intuition)

4. FINAL RECOMMENDATION
- One short paragraph explaining why this is the best optimized version

Rules:
- Do NOT output multiple recipes
- Do NOT ask questions
- Be precise and structured
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