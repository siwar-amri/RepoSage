
from pathlib import Path

from repomedic.parser import parse_file
from repomedic.chunker import create_chunks


def scan_repository(repo_path):
    repo_path = Path(repo_path)

    if not repo_path.is_dir():
        raise ValueError(f"Not a directory: {repo_path}")

    all_chunks = []

    for file_path in sorted(repo_path.rglob("*.py")):

        # Skip common generated/environment folders
        if any(
            part in {
                ".venv",
                "venv",
                "__pycache__",
                ".git"
            }
            for part in file_path.relative_to(repo_path).parts
        ):
            continue

        records = parse_file(file_path)
        chunks = create_chunks(records)

        for chunk in chunks:
            # Unique identifier across repository files
            relative_path = file_path.relative_to(repo_path)

            chunk["chunk_id"] = (
                f"{relative_path.as_posix()}::{chunk['name']}"
            )

        all_chunks.extend(chunks)

    return all_chunks
