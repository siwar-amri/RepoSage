
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.hybrid_search import reciprocal_rank_fusion


semantic_ranking = [
    "check_availability",
    "add_stock",
    "reserve_stock"
]

bm25_ranking = [
    "reserve_stock",
    "add_stock",
    "check_availability"
]

results = reciprocal_rank_fusion(
    rankings=[semantic_ranking, bm25_ranking],
    top_k=3
)

for rank, result in enumerate(results, start=1):
    print(
        rank,
        result["chunk_id"],
        round(result["score"], 6)
    )
