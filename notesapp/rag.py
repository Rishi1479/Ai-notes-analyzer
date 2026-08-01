import chromadb
from pypdf import PdfReader

_embedder = None
chroma_client = chromadb.PersistentClient(path="./chroma_store")


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def index_document(note_id, pdf_path):
    embedder = _get_embedder()
    collection = chroma_client.get_or_create_collection(f"note_{note_id}")
    text = extract_text(pdf_path)
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError(
            "Could not extract any text from the PDF. "
            "The file may be scanned/image-only or empty."
        )
    embeddings = embedder.encode(chunks).tolist()
    collection.upsert(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )


def retrieve_chunks(note_id, question, top_k=4):
    embedder = _get_embedder()
    collection = chroma_client.get_or_create_collection(f"note_{note_id}")
    q_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=q_embedding, n_results=top_k)
    return results["documents"][0]