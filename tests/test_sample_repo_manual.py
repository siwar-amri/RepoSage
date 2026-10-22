import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from repomedic.parser import parse_file
from repomedic.chunker import create_chunks


file_path = (
    project_root
    / "benchmarks"
    / "sample_repo"
    / "cart.py"
)

records = parse_file(file_path)
chunks = create_chunks(records)

print("Functions found:", len(chunks))

for chunk in chunks:
    print(
        chunk["name"],
        "|",
        chunk["file_path"]
    )
