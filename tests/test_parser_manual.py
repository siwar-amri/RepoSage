import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "src")
)

from repomedic.parser import parse_file


records = parse_file("src/examples/shopping_cart.py")

for record in records:
    print(record)
    print("-" * 40)
