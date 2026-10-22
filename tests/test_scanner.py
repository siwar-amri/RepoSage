
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.scanner import scan_repository


repo_path = project_root / "benchmarks" / "sample_repo"

chunks = scan_repository(repo_path)

print("Total chunks:", len(chunks))

for chunk in chunks:
    print(chunk["chunk_id"])
