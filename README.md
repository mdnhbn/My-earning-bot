# Telegram Income Bot

A mobile-manageable Telegram bot with user/admin panels, mandatory channel join verification, tasks, income, withdraws, vacation/maintenance modes, currency conversion, and basic payment stub. Designed to be copy-paste deployable.

## Features
- User: /register, channel join check, /tasks, /done <task_id>, /balance, /convert <CURRENCY>, /withdraw <amount>
- Admin: vacation/maintenance ON/OFF, set/list channels, add/remove/list tasks, task ON/OFF, ban/unban users, list/approve/reject withdraws, logs, stats

## Setup
1. Create a Telegram bot via BotFather and copy the token.
2. Edit `config.py`:
   - Put `TOKEN`
   - Set `ADMIN_IDS`
   - Optional: edit initial `REQUIRED_CHANNELS`
3. Ensure `data/` folder exists. Database will auto-create.
4. Install requirements: `pip install -r requirements.txt`
5. Run: `python bot.py`

## Notes
- For channel join verification, the bot must be able to `get_chat_member` of the channels:
  - Public channels (like @channel) are fine; if private, add the bot to channel.
- Payment integration is a stub. Replace `services/payment_api.py` with real provider if needed.
