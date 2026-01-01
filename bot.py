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
    app.add_handler(CommandHandler("convert", user_panel.convert))
    app.add_handler(CommandHandler("tasks", user_panel.tasks))
    app.add_handler(CommandHandler("done", user_panel.done))
    app.add_handler(CommandHandler("withdraw", user_panel.withdraw))

    # Admin commands
    app.add_handler(CommandHandler("vacation_on", admin_panel.vacation_on))
    app.add_handler(CommandHandler("vacation_off", admin_panel.vacation_off))
    app.add_handler(CommandHandler("maintenance_on", admin_panel.maintenance_on))
    app.add_handler(CommandHandler("maintenance_off", admin_panel.maintenance_off))

    app.add_handler(CommandHandler("setchannels", admin_panel.setchannels))
    app.add_handler(CommandHandler("listchannels", admin_panel.listchannels))

    app.add_handler(CommandHandler("addtask", admin_panel.addtask))
    app.add_handler(CommandHandler("removetask", admin_panel.removetask))
    app.add_handler(CommandHandler("listtasks", admin_panel.listtasks))
    app.add_handler(CommandHandler("taskon", admin_panel.taskon))
    app.add_handler(CommandHandler("taskoff", admin_panel.taskoff))

    app.add_handler(CommandHandler("banuser", admin_panel.banuser))
    app.add_handler(CommandHandler("unbanuser", admin_panel.unbanuser))

    app.add_handler(CommandHandler("listwithdraws", admin_panel.listwithdraws))
    app.add_handler(CommandHandler("approvewithdraw", admin_panel.approvewithdraw))
    app.add_handler(CommandHandler("rejectwithdraw", admin_panel.rejectwithdraw))

    app.add_handler(CommandHandler("logs", admin_panel.logs))
    app.add_handler(CommandHandler("stats", admin_panel.stats))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
