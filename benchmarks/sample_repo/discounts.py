
class DiscountEngine:
    def apply_percentage_discount(self, price, percentage):
        return price * (1 - percentage / 100)

    def apply_fixed_discount(self, price, amount):
        return max(0, price - amount)

    def validate_coupon(self, coupon, cart_total):
        return (
            coupon["active"]
            and cart_total >= coupon["minimum_order"]
        )

    def calculate_savings(self, original_price, final_price):
        return original_price - final_price
