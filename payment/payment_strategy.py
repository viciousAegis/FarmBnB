from paymentDao import PaymentDao
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class PaymentStrategy:
    def process_payment(self, user_id, amount, payment_info, total_price):
        pass

class UpiPaymentStrategy(PaymentStrategy):
    def process_payment(self, user_id, amount, payment_info, total_price):
        print(f"Processing UPI payment for user {user_id} with UPI ID: {payment_info}")
        MONGO_URI = os.environ.get("MONGO_URI")
        payment_dao = PaymentDao(MONGO_URI)
        payment_dao.increase_wallet_balance(user_id, amount)
        payment_dao.decrease_wallet_balance(user_id, total_price)
        return {"status": "success", "message": "UPI payment successful"}

class CardPaymentStrategy(PaymentStrategy):
    def process_payment(self, user_id, amount, payment_info, total_price):
        card_number = payment_info.get("card_number")
        cvv = payment_info.get("cvv")
        print(f"Processing card payment for user {user_id} with card number: {card_number} and CVV: ***")
        return {"status": "success", "message": "Card payment successful"}
