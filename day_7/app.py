from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os 

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

client = InferenceClient(api_key=HF_TOKEN)
response = client.chat_completion(
    model=MODEL_NAME,
    messages=[
              { "role":"user",
                "content":"hello"
              }
             ],
    max_tokens=100
)
print(response.choices[0].message.content)
