
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.evaluation import (
    recall_at_k,
    reciprocal_rank,
    mean_reciprocal_rank,
)


retrieved = [
    "ShoppingCart.add_item",
    "ShoppingCart.__init__",
    "ShoppingCart.total_price",
]

relevant = ["ShoppingCart.total_price"]

print("Recall@1:", recall_at_k(retrieved, relevant, 1))
print("Recall@3:", recall_at_k(retrieved, relevant, 3))
print("Reciprocal rank:", reciprocal_rank(retrieved, relevant))


rankings = [
    ["A", "B", "C"],
    ["B", "A", "C"],
    ["B", "C", "A"],
]

ground_truths = [
    ["A"],
    ["A"],
    ["A"],
]

print("MRR:", mean_reciprocal_rank(rankings, ground_truths))
