class Payment:
    def __init__(self, user_id, amount, payment_info):
        self.user_id = user_id
        self.amount = amount
        self.payment_info = payment_info

    def process_payment(self, payment_strategy):
        return payment_strategy.process_payment(self.user_id, self.amount, self.payment_info)
