
import ast
from pathlib import Path


def parse_file(file_path):
    path = Path(file_path)
    source_code = path.read_text(encoding="utf-8")
    tree = ast.parse(source_code, filename=str(path))

    records = []

    def visit_node(node, parent_name=""):
        if isinstance(node, ast.ClassDef):
            qualified_name = (
                f"{parent_name}.{node.name}"
                if parent_name else node.name
            )

            records.append({
                "name": qualified_name,
                "type": "class",
                "file_path": str(path),
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "code": ast.get_source_segment(source_code, node)
            })

            for child in node.body:
                visit_node(child, qualified_name)

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            qualified_name = (
                f"{parent_name}.{node.name}"
                if parent_name else node.name
            )

            records.append({
                "name": qualified_name,
                "type": "method" if parent_name else "function",
                "file_path": str(path),
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "code": ast.get_source_segment(source_code, node)
            })

            for child in node.body:
                visit_node(child, qualified_name)

        else:
            for child in ast.iter_child_nodes(node):
                visit_node(child, parent_name)

    visit_node(tree)

    return records
