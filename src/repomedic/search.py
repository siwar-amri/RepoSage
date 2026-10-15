
import numpy as np


def semantic_search(query, chunks, embedder, top_k=3):

    if not chunks:
        return []

    # Generate embeddings for our code chunks
    texts = [chunk["text"] for chunk in chunks]
    code_embeddings = embedder.embed_texts(texts)

    # Generate an embedding for the bug report
    query_embedding = embedder.embed_texts([query])[0]

    # Compare the query against every code chunk
    scores = code_embeddings @ query_embedding

    # Rank chunks from most to least similar
    ranked_indices = np.argsort(scores)[::-1]

    results = []

    for index in ranked_indices[:top_k]:
        results.append({
            "name": chunks[index]["name"],
            "file_path": chunks[index]["file_path"],
            "score": float(scores[index]),
            "code": chunks[index]["text"]
        })

    return results
