
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

benchmark_path = (
    project_root / "benchmarks" / "bug_reports.json"
)

with open(benchmark_path, "r", encoding="utf-8") as file:
    benchmark = json.load(file)

print("Number of bug reports:", len(benchmark))

for case in benchmark:
    print(
        case["id"],
        "->",
        case["relevant_functions"]
    )
