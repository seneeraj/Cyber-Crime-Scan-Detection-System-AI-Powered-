from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(texts):
    return model.encode(texts)

def create_faiss_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index

def search(index, query, texts):
    q_vec = model.encode([query])
    D, I = index.search(q_vec, k=3)
    return [texts[i] for i in I[0]]