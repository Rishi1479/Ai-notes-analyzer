import requests


def ask_llama(question, context, model="gemma4:e2b"):
    prompt = f"""Context:
{context}

Question:
{question}
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    return data["response"]