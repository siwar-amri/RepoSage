
def calculate_final_price(subtotal, tax_rate):
    return subtotal * (1 + tax_rate)


def validate_checkout(subtotal):
    return subtotal > 0
