import json
import os
import urllib.error
import urllib.request

# OAuth 2.0 Bearer token (RFC 6750). Groq uses your API key as the access token.
OAUTH2_ACCESS_TOKEN = os.environ["GROQ_API_KEY"]

request = urllib.request.Request(
    "https://api.groq.com/openai/v1/chat/completions",
    data=json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": "Answer to everything with a nice greeting message"}
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
    print(error.read().decode())
    raise

print(response["choices"][0]["message"]["content"])
