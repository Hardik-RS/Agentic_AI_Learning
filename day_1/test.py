from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
client = InferenceClient(token=os.getenv("HF_TOKEN"))
while True:
    prompt = input("You: ")

    if prompt.lower() == "exit":
        break
    response = client.chat_completion(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )   
    print(response.choices[0].message.content)
