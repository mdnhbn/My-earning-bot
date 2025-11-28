# services/payment_api.py
from core import database

def send_payment(withdraw_id: int) -> bool:
    """
    বাস্তব পেমেন্ট ইন্টিগ্রেশনের বদলে স্টাব।
    এডমিন approve করলে এটাকে success ধরবো।
    """
    try:
        database.set_withdraw_status(withdraw_id, "approved")
        return True
    except Exception:
        return False
