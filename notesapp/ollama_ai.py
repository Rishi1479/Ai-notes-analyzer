# import requests

# def ask_llama(question, context):

#     prompt = f"""
# Answer the question using only the provided document content.

# Document:
# {context}

# Question:
# {question}
# """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     data = response.json()

#     return data["response"]
import requests

def ask_llama(question, context):

    prompt = f"""
Context:
{context}

Question:
{question}
"""

    print("Sending prompt to Ollama...")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    print("Ollama response:", data["response"])

    return data["response"]