
import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.scanner import scan_repository


repo_path = project_root / "benchmarks" / "sample_repo"
benchmark_path = (
    project_root / "benchmarks" / "repository_bug_reports.json"
)

chunks = scan_repository(repo_path)

with open(benchmark_path, "r", encoding="utf-8") as file:
    benchmark = json.load(file)

available_ids = {chunk["chunk_id"] for chunk in chunks}

missing_ids = []

for case in benchmark:
    for relevant_id in case["relevant_functions"]:
        if relevant_id not in available_ids:
            missing_ids.append((case["id"], relevant_id))

print("Total code chunks:", len(chunks))
print("Total bug reports:", len(benchmark))
print("Unique chunk IDs:", len(available_ids))
print("Missing ground-truth IDs:", len(missing_ids))

if missing_ids:
    for bug_id, function_id in missing_ids:
        print(f"MISSING: {bug_id} -> {function_id}")
    raise AssertionError("Benchmark contains unknown function IDs")

assert len(available_ids) == len(chunks), "Duplicate chunk IDs found"
assert len(benchmark) == 15, "Expected 15 bug reports"

print("\nBenchmark validation PASSED!")
