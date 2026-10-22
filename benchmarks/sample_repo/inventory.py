
class InventoryManager:
    def __init__(self):
        self.stock = {}

    def add_stock(self, product_id, quantity):
        self.stock[product_id] = (
            self.stock.get(product_id, 0) + quantity
        )

    def check_availability(self, product_id, quantity):
        return self.stock.get(product_id, 0) >= quantity

    def reserve_stock(self, product_id, quantity):
        if not self.check_availability(product_id, quantity):
            return False

        self.stock[product_id] -= quantity
        return True

    def release_stock(self, product_id, quantity):
        self.add_stock(product_id, quantity)
