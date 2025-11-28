# panels/user_panel.py
from telegram import Update
from telegram.ext import ContextTypes
from core import database
from services.currency_api import convert_amount

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vacation/Maintenance চেক
    if database.is_vacation():
        await update.message.reply_text("🌴 বট বর্তমানে ভ্যাকেশন মোডে আছে। পরে চেষ্টা করুন।")
        return
    if database.is_maintenance():
        await update.message.reply_text("🛠️ বট বর্তমানে মেইনটেনেন্স মোডে আছে। পরে চেষ্টা করুন।")
        return

    user_id = update.effective_user.id
    database.add_user(user_id)

    # বাধ্যতামূলক চ্যানেল জয়েন চেক
    channels = database.get_channels()
    not_joined = []
    for ch in channels:
        try:
            member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
            # যদি 'left' হয় বা নেই, তখন not_joined
            if member.status in ["left"]:
                not_joined.append(ch)
        except Exception:
            # প্রাইভেট/অ্যাক্সেস না থাকলে জয়েন যাচাই ব্যর্থ; ইউজারকে যোগাযোগ করতে বলো
            not_joined.append(ch)

    if not_joined:
        msg = "❗ রেজিস্ট্রেশন সম্পন্ন করতে নিচের চ্যানেলগুলোতে জয়েন করুন:\n"
        for ch in not_joined:
            msg += f"- {ch}\n"
        msg += "\nজয়েন করার পর আবার /register লিখুন।"
        await update.message.reply_text(msg)
        return

    database.mark_registered(user_id)
    database.log_event(user_id, "register", "user registered successfully")
    await update.message.reply_text("✅ রেজিস্ট্রেশন সম্পন্ন হয়েছে!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return
    bal = database.get_balance(user_id)
    await update.message.reply_text(f"💰 আপনার ব্যালেন্স (SAR): {bal:.2f}")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return
    bal = database.get_balance(user_id)
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ ব্যবহার: /convert <CURRENCY> (যেমন /convert USD)")
        return
    to_cur = args[0].upper()
    converted = convert_amount(bal, to_cur, from_currency="SAR")
    await update.message.reply_text(f"💱 {bal:.2f} SAR ≈ {converted:.2f} {to_cur}")

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return

    if database.is_vacation() or database.is_maintenance():
        await update.message.reply_text("⏸️ বর্তমানে কাজ উপলভ্য নয়। পরে চেষ্টা করুন।")
        return

    rows = database.list_tasks(active_only=True)
    if not rows:
        await update.message.reply_text("📋 বর্তমানে কোনো কাজ নেই।")
    else:
        msg = "📋 কাজের তালিকা:\n"
        for t in rows:
            msg += f"ID {t[0]}: {t[1]} (Reward: {t[2]} SAR)\n"
        msg += "\nকাজ সম্পন্ন হলে /done <task_id> লিখে সাবমিট করুন।"
        await update.message.reply_text(msg)

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return

    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /done <task_id>")
        return

    try:
        tid = int(context.args[0])
        # রিওয়ার্ড বের করে ব্যালেন্স যোগ
        tasks = database.list_tasks(active_only=False)
        reward_map = {t[0]: t[2] for t in tasks}
        if tid not in reward_map:
            await update.message.reply_text("❌ ভুল task_id দেওয়া হয়েছে।")
            return
        reward = float(reward_map[tid])
        database.update_balance(user_id, reward)
        database.log_event(user_id, "task_done", f"task_id={tid}, reward={reward}")
        await update.message.reply_text(f"✅ কাজ সম্পন্ন! আপনার ব্যালেন্সে {reward:.2f} SAR যোগ হয়েছে।")
    except Exception:
        await update.message.reply_text("⚠️ ব্যবহার: /done <task_id>")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if database.is_banned(user_id):
        await update.message.reply_text("🚫 আপনি ব্লক করা হয়েছেন।")
        return

    bal = database.get_balance(user_id)
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ ব্যবহার: /withdraw <amount>")
        return
    try:
        amount = float(args[0])
        if amount <= 0:
            await update.message.reply_text("⚠️ পরিমাণ > 0 দিন।")
            return
        if amount > bal:
            await update.message.reply_text("❗ আপনার ব্যালেন্সের থেকে বেশি পরিমাণ দেওয়া হয়েছে।")
            return
        database.create_withdraw(user_id, amount)
        database.log_event(user_id, "withdraw_request", f"amount={amount}")
        await update.message.reply_text("📤 আপনার উইথড্রাল রিকোয়েস্ট সাবমিট হয়েছে। এডমিন অনুমোদন করলে টাকা পাঠানো হবে।")
    except Exception:
        await update.message.reply_text("⚠️ ব্যবহার: /withdraw <amount>")
