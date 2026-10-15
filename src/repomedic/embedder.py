
from sentence_transformers import SentenceTransformer


class CodeEmbedder:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_texts(self, texts):
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings
