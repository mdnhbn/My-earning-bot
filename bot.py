# bot.py
from telegram.ext import Application, CommandHandler
from config import TOKEN
from core import database
from panels import user_panel, admin_panel

def main():
    database.init_db()
    app = Application.builder().token(TOKEN).build()

    # User commands
    app.add_handler(CommandHandler("register", user_panel.register))
    app.add_handler(CommandHandler("balance", user_panel.balance))
    app.add_handler(CommandHandler("tasks", user_panel.tasks))
    app.add_handler(CommandHandler("withdraw", user_panel.withdraw))

    # Admin commands
    app.add_handler(CommandHandler("banuser", admin_panel.ban_user))
    app.add_handler(CommandHandler("unbanuser", admin_panel.unban_user))
    app.add_handler(CommandHandler("addtask", admin_panel.add_task))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
