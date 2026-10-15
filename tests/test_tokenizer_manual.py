
import sys
from pathlib import Path
from transformers import AutoTokenizer

# Locate our RepoMedic package
project_root = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(project_root / "src"))

from repomedic.parser import parse_file
from repomedic.chunker import create_chunks


# ==========================================
# EXPERIMENT 1: Basic tokenization
# ==========================================

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

code = "def total_price(self):"

tokens = tokenizer.tokenize(code)
code_token_ids = tokenizer.encode(code)

print("\n--- Basic Tokenization ---")
print("Original code:", code)
print("Tokens:", tokens)
print("Token IDs:", code_token_ids)
print("Number of token IDs:", len(code_token_ids))


# ==========================================
# EXPERIMENT 2: Attention masks and padding
# ==========================================

encoded = tokenizer(
    code,
    padding="max_length",
    truncation=True,
    max_length=16,
    return_tensors="pt"
)

print("\n--- Attention Mask ---")
print("Input IDs:", encoded["input_ids"])
print("Attention mask:", encoded["attention_mask"])


# ==========================================
# EXPERIMENT 3: Our RepoMedic code chunks
# ==========================================

file_path = project_root / "src" /  "examples" / "shopping_cart.py"

records = parse_file(file_path)
chunks = create_chunks(records)

print("\n--- RepoMedic Token Counts ---")

for chunk in chunks:
    chunk_token_ids = tokenizer.encode(
        chunk["text"],
        add_special_tokens=True
    )

    print(
        f"{chunk['name']}: {len(chunk_token_ids)} tokens"
    )


# ==========================================
# EXPERIMENT 4: Naming conventions
# ==========================================

examples = [
    "calculate total price",
    "calculate_total_price",
    "calculateTotalPrice"
]

print("\n--- Naming Convention Comparison ---")

for example in examples:
    print("Input:", example)
    print("Tokens:", tokenizer.tokenize(example))
    print()
