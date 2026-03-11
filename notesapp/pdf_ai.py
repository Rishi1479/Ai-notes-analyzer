from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import pipeline

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

qa_pipeline = pipeline(
    "text-generation",
    model="distilgpt2"
)


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks


def create_embeddings(chunks):

    embeddings = embed_model.encode(chunks)

    return embeddings


def answer_question(question, chunks, embeddings):

    q_embed = embed_model.encode([question])

    scores = cosine_similarity(q_embed, embeddings)

    best_chunk = chunks[np.argmax(scores)]

    prompt = f"""
    Answer the question based on the context.

    Context:
    {best_chunk}

    Question:
    {question}
    """

    result = qa_pipeline(prompt, max_length=200)

    return result[0]['generated_text']