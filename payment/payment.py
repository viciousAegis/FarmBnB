class Payment:
    def __init__(self, user_id, amount, payment_info, total_price):
        self.user_id = user_id
        self.amount = amount
        self.payment_info = payment_info
        self.total_price = total_price

    def process_payment(self, payment_strategy):
        return payment_strategy.process_payment(self.user_id, self.amount, self.payment_info, self.total_price)
