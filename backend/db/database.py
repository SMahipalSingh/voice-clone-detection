import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "history.db"))

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_size_kb REAL DEFAULT 0,
            duration_sec REAL DEFAULT 0,
            risk_score INTEGER NOT NULL,
            verdict TEXT NOT NULL,
            threat_tier TEXT,
            scenario TEXT NOT NULL,
            block_hash TEXT NOT NULL,
            audio_sha256 TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_history(filename: str, risk_score: int, verdict: str, scenario: str, timestamp: str,
                 block_hash: str, file_size_kb: float = 0.0, duration_sec: float = 0.0,
                 threat_tier: str = "", audio_sha256: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (filename, file_size_kb, duration_sec, risk_score, verdict, threat_tier, scenario, block_hash, audio_sha256, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (filename, file_size_kb, duration_sec, risk_score, verdict, threat_tier, scenario, block_hash, audio_sha256, timestamp))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_history(limit: int = 50) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
