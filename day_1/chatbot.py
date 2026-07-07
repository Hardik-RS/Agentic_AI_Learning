import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
print(HF_TOKEN)
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

url = "https://router.huggingface.co/v1/chat/completions"

while True:
    prompt = input("You: ")

    if prompt.lower() == "exit":
        break

    response = requests.post(
        url,
        headers=headers,
        json={
            "model": os.getenv("MODEL_NAME"),
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]
    print("Bot:", answer)