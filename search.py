from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings, chunks

def search_index(index, query, chunks, top_k=3):
    q_vec = model.encode([query])
    D, I = index.search(np.array(q_vec), top_k)
    return [chunks[i] for i in I[0]]
  