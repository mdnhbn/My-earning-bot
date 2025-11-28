# panels/user_panel.py
from telegram import Update
from telegram.ext import ContextTypes
from core import database
import config

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if config.VACATION_MODE:
        await update.message.reply_text("🌴 বট বর্তমানে ভ্যাকেশন মোডে আছে। পরে চেষ্টা করুন।")
        return
    if config.MAINTENANCE_MODE:
        await update.message.reply_text("🛠️ বট বর্তমানে মেইনটেনেন্স মোডে আছে। পরে চেষ্টা করুন।")
        return
    user_id = update.effective_user.id
    database.add_user(user_id)
    await update.message.reply_text("✅ রেজিস্ট্রেশন সম্পন্ন হয়েছে!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return
    bal = database.get_balance(user_id)
    await update.message.reply_text(f"💰 আপনার ব্যালেন্স: {bal}")

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return
    tasks = database.list_tasks()
    if not tasks:
        await update.message.reply_text("📋 বর্তমানে কোনো কাজ নেই।")
    else:
        msg = "📋 কাজের তালিকা:\n"
        for t in tasks:
            msg += f"ID {t[0]}: {t[1]} (Reward: {t[2]})\n"
        await update.message.reply_text(msg)

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📤 আপনার উইথড্রাল রিকোয়েস্ট সাবমিট হয়েছে। এডমিন অনুমোদন করলে টাকা পাঠানো হবে।")
