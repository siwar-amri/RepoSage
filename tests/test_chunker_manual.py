
import sys
from pathlib import Path

# Step 1: Find the main project folder
project_root = Path(__file__).resolve().parent.parent

# Step 2: Tell Python where our package is located
sys.path.insert(0, str(project_root / "src"))

# Step 3: Import our components
from repomedic.parser import parse_file
from repomedic.chunker import create_chunks

# Step 4: Select the file we want to analyze
file_path = project_root / "src" / "examples" / "shopping_cart.py"

# Step 5: Parse the file
records = parse_file(file_path)

# Step 6: Convert records into chunks
chunks = create_chunks(records)

# Step 7: Display the results
for chunk in chunks:
    print("=" * 50)
    print(chunk["text"])
