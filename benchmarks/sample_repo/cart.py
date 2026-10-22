
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        self.items.append({
            "product": product,
            "quantity": quantity
        })

    def remove_item(self, product_id):
        self.items = [
            item for item in self.items
            if item["product"]["id"] != product_id
        ]

    def calculate_subtotal(self):
        return sum(
            item["product"]["price"] * item["quantity"]
            for item in self.items
        )

    def count_items(self):
        return sum(
            item["quantity"]
            for item in self.items
        )
