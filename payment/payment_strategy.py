class PaymentStrategy:
    def process_payment(self, user_id, amount, payment_info):
        pass

class UpiPaymentStrategy(PaymentStrategy):
    def process_payment(self, user_id, amount, payment_info):
        print(f"Processing UPI payment for user {user_id} with UPI ID: {payment_info}")
        return {"status": "success", "message": "UPI payment successful"}

class CardPaymentStrategy(PaymentStrategy):
    def process_payment(self, user_id, amount, payment_info):
        card_number = payment_info.get("card_number")
        cvv = payment_info.get("cvv")
        print(f"Processing card payment for user {user_id} with card number: {card_number} and CVV: ***")
        return {"status": "success", "message": "Card payment successful"}
