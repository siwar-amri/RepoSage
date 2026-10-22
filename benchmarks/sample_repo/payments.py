
class PaymentProcessor:
    def validate_payment(self, amount, payment_method):
        return amount > 0 and payment_method is not None

    def calculate_transaction_fee(self, amount, fee_rate):
        return amount * fee_rate

    def process_refund(self, payment_amount, refund_amount):
        if refund_amount > payment_amount:
            raise ValueError("Refund exceeds payment amount")

        return payment_amount - refund_amount

    def calculate_total_charge(self, amount, fee):
        return amount + fee
