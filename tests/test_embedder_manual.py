
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.parser import parse_file
from repomedic.chunker import create_chunks
from repomedic.embedder import CodeEmbedder


# Step 1: Parse our example repository file
file_path = project_root / "src" / "examples" / "shopping_cart.py"
records = parse_file(file_path)

# Step 2: Create searchable chunks
chunks = create_chunks(records)

# Step 3: Extract the text from each chunk
texts = [chunk["text"] for chunk in chunks]

# Step 4: Generate embeddings
embedder = CodeEmbedder()
embeddings = embedder.embed_texts(texts)

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

# Display part of the first embedding
print("First embedding (first 10 values):")
print(embeddings[0][:10])



import numpy as np

sentences = [
    "Calculate the total price of a shopping cart",
    "Find the sum of all product prices",
    "Connect to the database server",
    "The shopping cart crashes when calculating the final amount"
]

vectors = embedder.embed_texts(sentences)

similarity_matrix = vectors @ vectors.T

print("\nSimilarity matrix:")
print(np.round(similarity_matrix, 3))
