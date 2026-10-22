
import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.scanner import scan_repository
from repomedic.embedder import CodeEmbedder
from repomedic.search import semantic_search
from repomedic.bm25_search import BM25Searcher
from repomedic.hybrid_search import reciprocal_rank_fusion
from repomedic.evaluation import recall_at_k, reciprocal_rank


# =====================================
# 1. Load repository and benchmark
# =====================================

repo_path = project_root / "benchmarks" / "sample_repo"
benchmark_path = (
    project_root / "benchmarks" / "repository_bug_reports.json"
)

chunks = scan_repository(repo_path)

with open(benchmark_path, "r", encoding="utf-8") as file:
    benchmark = json.load(file)

available_ids = {chunk["chunk_id"] for chunk in chunks}

for case in benchmark:
    for function_id in case["relevant_functions"]:
        if function_id not in available_ids:
            raise ValueError(f"Unknown function ID: {function_id}")

# Match semantic results to unique repository IDs
id_lookup = {
    (chunk["name"], str(chunk["file_path"])): chunk["chunk_id"]
    for chunk in chunks
}


# =====================================
# 2. Initialize retrieval systems
# =====================================

embedder = CodeEmbedder()
bm25 = BM25Searcher(chunks)

all_scores = []
results_by_difficulty = {}


# =====================================
# 3. Evaluate all bug reports
# =====================================

for case in benchmark:
    query = case["bug_report"]
    relevant = case["relevant_functions"]

    # Semantic ranking
    semantic_results = semantic_search(
        query=query,
        chunks=chunks,
        embedder=embedder,
        top_k=len(chunks)
    )

    semantic_ids = [
        id_lookup[(r["name"], str(r["file_path"]))]
        for r in semantic_results
    ]

    # BM25 ranking
    bm25_results = bm25.search(
        query=query,
        top_k=len(chunks)
    )

    bm25_ids = [
        r["chunk_id"]
        for r in bm25_results
    ]

    # Hybrid ranking using RRF
    hybrid_results = reciprocal_rank_fusion(
        rankings=[semantic_ids, bm25_ids],
        k=60,
        top_k=len(chunks)
    )

    hybrid_ids = [
        r["chunk_id"]
        for r in hybrid_results
    ]

    scores = {
        "recall_1": recall_at_k(hybrid_ids, relevant, 1),
        "recall_3": recall_at_k(hybrid_ids, relevant, 3),
        "recall_5": recall_at_k(hybrid_ids, relevant, 5),
        "rr": reciprocal_rank(hybrid_ids, relevant)
    }

    all_scores.append(scores)

    difficulty = case["difficulty"]
    results_by_difficulty.setdefault(difficulty, []).append(scores)

    print(f"\n{case['id']} ({difficulty})")
    print("Expected:", relevant)
    print("Semantic top 3:", semantic_ids[:3])
    print("BM25 top 3:", bm25_ids[:3])
    print("Hybrid top 3:", hybrid_ids[:3])
    print("Recall@1:", scores["recall_1"])
    print("Recall@3:", scores["recall_3"])
    print("Recall@5:", scores["recall_5"])
    print("RR:", round(scores["rr"], 3))


# =====================================
# 4. Print summary
# =====================================

def print_summary(label, scores):
    if not scores:
        return

    print(f"\n{label} (n={len(scores)})")

    for metric in ["recall_1", "recall_3", "recall_5", "rr"]:
        average = sum(s[metric] for s in scores) / len(scores)
        print(f"  {metric}: {average:.3f}")


print("\n========== HYBRID RESULTS ==========")

print_summary("All reports", all_scores)

for difficulty in ["easy", "medium", "hard"]:
    print_summary(
        difficulty.capitalize(),
        results_by_difficulty.get(difficulty, [])
    )
