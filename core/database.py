# core/database.py
import sqlite3
from typing import List, Tuple

DB_PATH = "data/bot.db"

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = _connect()
    c = conn.cursor()

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0,
            banned INTEGER DEFAULT 0,
            registered INTEGER DEFAULT 0
        )
    """)

    # Withdraw requests
    c.execute("""
        CREATE TABLE IF NOT EXISTS withdraws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tasks
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            reward REAL,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Required channels list
    c.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    """)

    # Settings: vacation, maintenance
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    # Ensure default settings
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('vacation', '0')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance', '0')")

    # Logs
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            detail TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed initial required channels from config once
    from config import REQUIRED_CHANNELS
    for ch in REQUIRED_CHANNELS:
        try:
            c.execute("INSERT OR IGNORE INTO channels (username) VALUES (?)", (ch,))
        except:
            pass

    conn.commit()
    conn.close()

# Users
def add_user(user_id: int):
    conn = _connect()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def mark_registered(user_id: int):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE users SET registered=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_registered(user_id: int) -> bool:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT registered FROM users WHERE user_id=?", (user_id,))
    r = c.fetchone()
    conn.close()
    return bool(r and r[0] == 1)

def update_balance(user_id: int, amount: float):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()

def get_balance(user_id: int) -> float:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return float(result[0]) if result else 0.0

def ban_user(user_id: int):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE users SET banned=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id: int):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE users SET banned=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_banned(user_id: int) -> bool:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT banned FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return bool(result and result[0] == 1)

# Withdraws
def create_withdraw(user_id: int, amount: float):
    conn = _connect()
    c = conn.cursor()
    c.execute("INSERT INTO withdraws (user_id, amount) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    conn.close()

def list_withdraws(status: str = "pending") -> List[Tuple]:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT id, user_id, amount, status, created_at FROM withdraws WHERE status=?", (status,))
    rows = c.fetchall()
    conn.close()
    return rows

def set_withdraw_status(wid: int, status: str):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE withdraws SET status=? WHERE id=?", (status, wid))
    conn.commit()
    conn.close()

# Tasks
def add_task(description: str, reward: float):
    conn = _connect()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description, reward) VALUES (?, ?)", (description, reward))
    conn.commit()
    conn.close()

def remove_task(task_id: int):
    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def list_tasks(active_only: bool = True) -> List[Tuple]:
    conn = _connect()
    c = conn.cursor()
    if active_only:
        c.execute("SELECT id, description, reward FROM tasks WHERE active=1 ORDER BY id DESC")
    else:
        c.execute("SELECT id, description, reward, active FROM tasks ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def set_task_active(task_id: int, active: bool):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE tasks SET active=? WHERE id=?", (1 if active else 0, task_id))
    conn.commit()
    conn.close()

# Channels
def set_channels(chs: List[str]):
    conn = _connect()
    c = conn.cursor()
    c.execute("DELETE FROM channels")
    for ch in chs:
        c.execute("INSERT OR IGNORE INTO channels (username) VALUES (?)", (ch,))
    conn.commit()
    conn.close()

def get_channels() -> List[str]:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT username FROM channels")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

# Settings
def set_setting(key: str, value: str):
    conn = _connect()
    c = conn.cursor()
    c.execute("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
    conn.commit()
    conn.close()

def get_setting(key: str) -> str:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else "0"

def is_vacation() -> bool:
    return get_setting("vacation") == "1"

def is_maintenance() -> bool:
    return get_setting("maintenance") == "1"

# Logs
def log_event(user_id: int, action: str, detail: str = ""):
    conn = _connect()
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, action, detail) VALUES (?, ?, ?)", (user_id, action, detail))
    conn.commit()
    conn.close()

def get_logs(limit: int = 50) -> List[Tuple]:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT id, user_id, action, detail, created_at FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# Stats
def get_stats() -> Tuple[int, float, int]:
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0) FROM users")
    user_count, total_balance = c.fetchone()
    c.execute("SELECT COUNT(*) FROM withdraws WHERE status='approved'")
    approved_withdraws = c.fetchone()[0]
    conn.close()
    return int(user_count or 0), float(total_balance or 0.0), int(approved_withdraws or 0)
