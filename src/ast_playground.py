import ast 

source_code = """

class shopping_shelf:
    def __init__(self):
        self.items=[]

    def add_item(self, item):
        self.items.append(item)

    def calculate_total_price(self):
        return sum(self.item*price for item in shopping_shelf)

"""

tree= ast.parse(source_code)

for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        print("class namme is: ", node.name)
    if isinstance(node, ast.FunctionDef):
        print("function", node.name)
        


