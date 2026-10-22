
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.scanner import scan_repository
from repomedic.bm25_search import BM25Searcher


repo_path = project_root / "benchmarks" / "sample_repo"

chunks = scan_repository(repo_path)

searcher = BM25Searcher(chunks)

query = "The inventory system fails to reserve stock"

results = searcher.search(query, top_k=5)

print("Query:", query)

for rank, result in enumerate(results, start=1):
    print(
        rank,
        result["chunk_id"],
        round(result["score"], 3)
    )
