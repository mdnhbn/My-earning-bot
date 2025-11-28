# panels/admin_panel.py
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS
from core import database

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        user_id = int(context.args[0])
        database.ban_user(user_id)
        await update.message.reply_text(f"🚫 ইউজার {user_id} ব্লক করা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /banuser <user_id>")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        user_id = int(context.args[0])
        database.unban_user(user_id)
        await update.message.reply_text(f"✅ ইউজার {user_id} আনব্লক করা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /unbanuser <user_id>")

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        description = context.args[0]
        reward = float(context.args[1])
        database.add_task(description, reward)
        await update.message.reply_text(f"📋 নতুন কাজ যোগ হয়েছে: {description} (Reward: {reward})")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /addtask <description> <reward>")
