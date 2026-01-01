# panels/admin_panel.py
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS
from core import database
from services.payment_api import send_payment

def _is_admin(uid: int) -> bool:
    return uid in ADMIN_IDS

# Modes
async def vacation_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    database.set_setting("vacation", "1")
    await update.message.reply_text("🌴 Vacation mode: ON")

async def vacation_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    database.set_setting("vacation", "0")
    await update.message.reply_text("🌴 Vacation mode: OFF")

async def maintenance_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    database.set_setting("maintenance", "1")
    await update.message.reply_text("🛠️ Maintenance mode: ON")

async def maintenance_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    database.set_setting("maintenance", "0")
    await update.message.reply_text("🛠️ Maintenance mode: OFF")

# Channels
async def setchannels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /setchannels @ch1 @ch2 @ch3 ...")
        return
    chs = [a for a in context.args if a.startswith("@")]
    if not chs:
        await update.message.reply_text("⚠️ অন্তত ১টি @channel দিন।")
        return
    database.set_channels(chs)
    await update.message.reply_text("✅ বাধ্যতামূলক চ্যানেল লিস্ট আপডেট হয়েছে।")

async def listchannels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    chs = database.get_channels()
    if not chs:
        await update.message.reply_text("📭 কোনো চ্যানেল সেট করা নেই।")
        return
    await update.message.reply_text("📌 বাধ্যতামূলক চ্যানেল:\n" + "\n".join(chs))

# Tasks
async def addtask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ ব্যবহার: /addtask <description> <reward>")
        return
    description = context.args[0]
    try:
        reward = float(context.args[1])
    except:
        await update.message.reply_text("⚠️ reward সংখ্যায় দিন।")
        return
    database.add_task(description, reward)
    await update.message.reply_text(f"📋 নতুন কাজ যোগ হয়েছে: {description} (Reward: {reward} SAR)")

async def removetask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /removetask <task_id>")
        return
    try:
        tid = int(context.args[0])
        database.remove_task(tid)
        await update.message.reply_text(f"🗑️ কাজ {tid} মুছে ফেলা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /removetask <task_id>")

async def listtasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    rows = database.list_tasks(active_only=False)
    if not rows:
        await update.message.reply_text("📋 কোনো কাজ নেই।")
    else:
        msg = "📋 সব কাজ:\n"
        for t in rows:
            msg += f"ID {t[0]}: {t[1]} (Reward: {t[2]} SAR) | Active: {t[3]}\n"
        await update.message.reply_text(msg)

async def taskon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /taskon <task_id>")
        return
    try:
        tid = int(context.args[0])
        database.set_task_active(tid, True)
        await update.message.reply_text(f"✅ কাজ {tid} সক্রিয় করা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /taskon <task_id>")

async def taskoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /taskoff <task_id>")
        return
    try:
        tid = int(context.args[0])
        database.set_task_active(tid, False)
        await update.message.reply_text(f"⏸️ কাজ {tid} নিষ্ক্রিয় করা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /taskoff <task_id>")

# User management
async def banuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /banuser <user_id>")
        return
    try:
        uid = int(context.args[0])
        database.ban_user(uid)
        await update.message.reply_text(f"🚫 ইউজার {uid} ব্লক করা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /banuser <user_id>")

async def unbanuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /unbanuser <user_id>")
        return
    try:
        uid = int(context.args[0])
        database.unban_user(uid)
        await update.message.reply_text(f"✅ ইউজার {uid} আনব্লক করা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /unbanuser <user_id>")

# Withdraw approvals
async def listwithdraws(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    rows = database.list_withdraws(status="pending")
    if not rows:
        await update.message.reply_text("📭 কোনো পেন্ডিং উইথড্রাল নেই।")
        return
    msg = "⏳ Pending withdraws:\n"
    for w in rows:
        msg += f"ID {w[0]} | User {w[1]} | Amount {w[2]} SAR | {w[4]}\n"
    await update.message.reply_text(msg)

async def approvewithdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /approvewithdraw <withdraw_id>")
        return
    try:
        wid = int(context.args[0])
        ok = send_payment(wid)
        if ok:
            await update.message.reply_text(f"✅ Withdraw {wid} approved and processed.")
        else:
            await update.message.reply_text(f"❌ Withdraw {wid} approve করতে সমস্যা হয়েছে।")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /approvewithdraw <withdraw_id>")

async def rejectwithdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /rejectwithdraw <withdraw_id>")
        return
    try:
        wid = int(context.args[0])
        database.set_withdraw_status(wid, "rejected")
        await update.message.reply_text(f"❎ Withdraw {wid} rejected.")
    except:
        await update.message.reply_text("⚠️ ব্যবহার: /rejectwithdraw <withdraw_id>")

# Logs & Stats
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    rows = database.get_logs(limit=50)
    if not rows:
        await update.message.reply_text("📭 কোনো লগ নেই।")
        return
    msg = "🧾 Logs (last 50):\n"
    for lg in rows:
        msg += f"[{lg[4]}] User {lg[1]}: {lg[2]} ({lg[3]})\n"
    await update.message.reply_text(msg[:4000])  # Telegram limit

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update.effective_user.id): return
    users, total_balance, approved_withdraws = database.get_stats()
    await update.message.reply_text(
        f"📊 Stats:\nUsers: {users}\nTotal Balance (SAR): {total_balance:.2f}\nApproved Withdraws: {approved_withdraws}"
    )
