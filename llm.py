import requests
from config import OLLAMA_URL

def generate_summary(prompt: str, model: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    return response.json()["response"]
