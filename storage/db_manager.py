"""
Quản lý lưu log và đơn hàng bằng sqlite cho demo.
"""
import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).resolve().parents[1] / "fastfood_chat.db"

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        direction TEXT,
        content TEXT,
        metadata TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_json TEXT,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_log(direction: str, content: dict, metadata: dict = None):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO logs (direction, content, metadata) VALUES (?,?,?)",
              (direction, json.dumps(content, ensure_ascii=False), json.dumps(metadata or {}, ensure_ascii=False)))
    conn.commit()
    conn.close()

def save_order(order_obj: dict):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO orders (order_json, status) VALUES (?,?)",
              (json.dumps(order_obj, ensure_ascii=False), "created"))
    conn.commit()
    oid = c.lastrowid
    conn.close()
    return oid

def get_orders(limit=20):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT id, order_json, status, created_at FROM orders ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
