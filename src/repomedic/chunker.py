
def create_chunks(records):
    chunks = []

    for record in records:
        if record["type"] not in ("function", "method"):
            continue

        chunk_text = (
            f"File: {record['file_path']}\n"
            f"Symbol: {record['name']}\n"
            f"Type: {record['type']}\n\n"
            f"Code:\n{record['code']}"
        )

        chunk = {
            "name": record["name"],
            "file_path": record["file_path"],
            "start_line": record["start_line"],
            "end_line": record["end_line"],
            "text": chunk_text
        }

        chunks.append(chunk)

    return chunks
