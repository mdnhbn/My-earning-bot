# services/currency_api.py
import requests
from config import CURRENCY_API_BASE

def convert_amount(amount: float, to_currency: str, from_currency: str = "SAR") -> float:
    """
    amount: ব্যালেন্স পরিমাণ
    to_currency: যে কারেন্সিতে দেখতে চাও (e.g., 'USD', 'INR')
    from_currency: মূল কারেন্সি (ডিফল্ট 'SAR')
    """
    try:
        params = {"from": from_currency.upper(), "to": to_currency.upper(), "amount": amount}
        r = requests.get(CURRENCY_API_BASE, params=params, timeout=10)
        data = r.json()
        return float(data.get("result", 0.0))
    except Exception:
        return 0.0
