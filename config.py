# config.py
# Bot settings and admin configuration

TOKEN = "YOUR_BOTFATHER_TOKEN"   # BotFather থেকে পাওয়া টোকেন এখানে বসাও
ADMIN_IDS = [123456789]          # এডমিনদের টেলিগ্রাম ইউজার আইডি বসাও (list)

# প্রাথমিক বাধ্যতামূলক চ্যানেল — কমান্ড দিয়ে পরেও আপডেট করা যাবে
REQUIRED_CHANNELS = [
    "@channel1",
    "@channel2",
    "@channel3",
    "@channel4",
    "@channel5"
]

# কারেন্সি কনভার্সন API (exchangerate.host ব্যবহার করা সহজ এবং ফ্রি)
CURRENCY_API_BASE = "https://api.exchangerate.host/convert"

# পেমেন্ট API স্টাব: এখানে আসল পেমেন্ট গেটওয়ে ইন্টিগ্রেট করলে কী/ক্রেডেনশিয়াল রাখতে পারো
PAYMENT_PROVIDER = "stub"  # 'stub' রেখে দাও; বাস্তব পেমেন্ট হলে 'bkash', 'paypal' ইত্যাদি
