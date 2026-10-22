
import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.scanner import scan_repository
from repomedic.bm25_search import BM25Searcher
from repomedic.evaluation import recall_at_k, reciprocal_rank


# 1. Load repository and benchmark
repo_path = project_root / "benchmarks" / "sample_repo"
benchmark_path = (
    project_root / "benchmarks" / "repository_bug_reports.json"
)

chunks = scan_repository(repo_path)

with open(benchmark_path, "r", encoding="utf-8") as file:
    benchmark = json.load(file)


# 2. Initialize BM25 once
searcher = BM25Searcher(chunks)

all_scores = []
results_by_difficulty = {}


# 3. Evaluate every bug report
for case in benchmark:

    results = searcher.search(
        query=case["bug_report"],
        top_k=len(chunks)
    )

    retrieved = [
        result["chunk_id"]
        for result in results
    ]

    relevant = case["relevant_functions"]

    scores = {
        "recall_1": recall_at_k(retrieved, relevant, 1),
        "recall_3": recall_at_k(retrieved, relevant, 3),
        "recall_5": recall_at_k(retrieved, relevant, 5),
        "rr": reciprocal_rank(retrieved, relevant)
    }

    all_scores.append(scores)

    difficulty = case["difficulty"]

    results_by_difficulty.setdefault(
        difficulty, []
    ).append(scores)

    print(f"\n{case['id']} ({difficulty})")
    print("Expected:", relevant)
    print("Top 3:", retrieved[:3])
    print("Recall@1:", scores["recall_1"])
    print("Recall@3:", scores["recall_3"])
    print("Recall@5:", scores["recall_5"])
    print("RR:", round(scores["rr"], 3))


# 4. Print aggregate results
def print_summary(label, scores):
    if not scores:
        return

    print(f"\n{label} (n={len(scores)})")

    for metric in [
        "recall_1",
        "recall_3",
        "recall_5",
        "rr"
    ]:
        average = sum(
            s[metric] for s in scores
        ) / len(scores)

        print(f"  {metric}: {average:.3f}")


print("\n========== BM25 RESULTS ==========")

print_summary("All reports", all_scores)

for difficulty in ["easy", "medium", "hard"]:
    print_summary(
        difficulty.capitalize(),
        results_by_difficulty.get(difficulty, [])
    )
