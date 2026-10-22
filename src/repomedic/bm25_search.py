
import re

from rank_bm25 import BM25Okapi


def tokenize(text):
    # Split camelCase and PascalCase identifiers
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)

    # Split snake_case identifiers
    text = text.replace("_", " ")

    # Extract lowercase word tokens
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Searcher:
    def __init__(self, chunks):
        self.chunks = chunks

        self.tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def search(self, query, top_k=5):
        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for i in ranked_indices[:top_k]:
            results.append({
                "chunk_id": self.chunks[i]["chunk_id"],
                "name": self.chunks[i]["name"],
                "score": float(scores[i])
            })

        return results
