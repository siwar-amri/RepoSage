
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.parser import parse_file
from repomedic.chunker import create_chunks
from repomedic.embedder import CodeEmbedder
from repomedic.search import semantic_search


# Parse and chunk our example code
file_path = project_root / "src" / "examples" / "shopping_cart.py"

records = parse_file(file_path)
chunks = create_chunks(records)

# Load our embedding model
embedder = CodeEmbedder()

# Describe a bug in natural language
query = "A new product is not being added to the shopping cart"

results = semantic_search(
    query=query,
    chunks=chunks,
    embedder=embedder,
    top_k=3
)

print("\nBUG REPORT:", query)
print("\nMOST RELEVANT FUNCTIONS:")

for rank, result in enumerate(results, start=1):
    print(f"\nRank {rank}: {result['name']}")
    print(f"Similarity: {result['score']:.3f}")
    print(f"File: {result['file_path']}")
