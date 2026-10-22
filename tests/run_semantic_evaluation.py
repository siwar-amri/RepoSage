
import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.parser import parse_file
from repomedic.chunker import create_chunks
from repomedic.embedder import CodeEmbedder
from repomedic.search import semantic_search
from repomedic.evaluation import (
    recall_at_k,
    reciprocal_rank
)


# =====================================
# 1. Load benchmark dataset
# =====================================

benchmark_path = project_root / "benchmarks" / "bug_reports.json"

with open(benchmark_path, "r", encoding="utf-8") as file:
    benchmark = json.load(file)


# =====================================
# 2. Parse and chunk source code
# =====================================

file_path = project_root / "examples" / "shopping_cart.py"

records = parse_file(file_path)
chunks = create_chunks(records)

print("\n=== ACTUAL CHUNK NAMES ===")
for chunk in chunks:
    print(repr(chunk["name"]))

print("\n=== EXPECTED FUNCTION NAMES ===")
for case in benchmark:
    print(case["id"], repr(case["relevant_functions"]))

print("Number of code chunks:", len(chunks))
print("Number of bug reports:", len(benchmark))


# =====================================
# 3. Load embedding model
# =====================================

embedder = CodeEmbedder()


# =====================================
# 4. Evaluate each bug report
# =====================================

recall_1_scores = []
recall_3_scores = []
rr_scores = []

for case in benchmark:

    query = case["bug_report"]
    relevant = case["relevant_functions"]

    results = semantic_search(
        query=query,
        chunks=chunks,
        embedder=embedder,
        top_k=len(chunks)
    )

    retrieved = [result["name"] for result in results]

    r1 = recall_at_k(retrieved, relevant, 1)
    r3 = recall_at_k(retrieved, relevant, 3)
    rr = reciprocal_rank(retrieved, relevant)

    recall_1_scores.append(r1)
    recall_3_scores.append(r3)
    rr_scores.append(rr)

    print(f"\n{case['id']}: {query}")
    print("Expected:", relevant)
    print("Retrieved:", retrieved)
    print(f"Recall@1: {r1:.3f}")
    print(f"Recall@3: {r3:.3f}")
    print(f"RR: {rr:.3f}")


# =====================================
# 5. Aggregate results
# =====================================

mean_recall_1 = sum(recall_1_scores) / len(recall_1_scores)
mean_recall_3 = sum(recall_3_scores) / len(recall_3_scores)
mrr = sum(rr_scores) / len(rr_scores)

print("\n========== FINAL RESULTS ==========")
print(f"Mean Recall@1: {mean_recall_1:.3f}")
print(f"Mean Recall@3: {mean_recall_3:.3f}")
print(f"MRR: {mrr:.3f}")
