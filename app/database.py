import sqlite3
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Database folder
DATABASE_DIR = BASE_DIR / "database"


# SQLite database file
DATABASE_PATH = DATABASE_DIR / "honeypot.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    # Make sure the database directory exists
    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    # Allows rows to behave like dictionaries
    connection.row_factory = sqlite3.Row

    return connection


def init_database():
    """
    Create the honeypot request_logs table
    if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            ip TEXT,

            method TEXT,

            path TEXT,

            risk TEXT,

            attack TEXT,

            user_agent TEXT

        )
    """)

    connection.commit()

    connection.close()

def get_recent_requests(limit=100):
    """
    Return the most recent honeypot requests
    stored in the SQLite database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            ip,
            method,
            path,
            risk,
            attack,
            user_agent
        FROM request_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    requests = []

    for row in rows:

        requests.append({
            "id": row["id"],
            "time": row["timestamp"],
            "ip": row["ip"],
            "method": row["method"],
            "path": row["path"],
            "risk": row["risk"],
            "attack": row["attack"],
            "user_agent": row["user_agent"]
        })

    return requests


def get_attack_logs(limit=100):
    """
    Return recent requests that were classified
    as actual security events.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            ip,
            method,
            path,
            risk,
            attack,
            user_agent
        FROM request_logs
        WHERE attack != 'Normal Request'
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    attacks = []

    for row in rows:

        attacks.append({
            "id": row["id"],
            "time": row["timestamp"],
            "ip": row["ip"],
            "method": row["method"],
            "path": row["path"],
            "risk": row["risk"],
            "attack": row["attack"],
            "user_agent": row["user_agent"]
        })

    return attacks

def get_security_stats():
    """
    Calculate security statistics from the SQLite database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # Total requests
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM request_logs
    """)

    total_requests = cursor.fetchone()["count"]


    # Suspicious IPs
    cursor.execute("""
        SELECT COUNT(DISTINCT ip) AS count
        FROM request_logs
        WHERE risk IN ('High', 'Medium')
    """)

    suspicious_ips = cursor.fetchone()["count"]


    # High-risk requests
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM request_logs
        WHERE risk = 'High'
    """)

    high_risk = cursor.fetchone()["count"]


    # Honeypot hits
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM request_logs
        WHERE attack != 'Normal Request'
    """)

    honeypot_hits = cursor.fetchone()["count"]


    connection.close()


    return {
        "attacks_today": total_requests,
        "suspicious_ips": suspicious_ips,
        "high_risk": high_risk,
        "honeypot_hits": honeypot_hits
    }

def get_attack_summary():
    """
    Count detected attacks by attack type.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            attack,
            COUNT(*) AS count
        FROM request_logs
        WHERE attack != 'Normal Request'
        GROUP BY attack
        ORDER BY count DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    summary = {}

    for row in rows:
        summary[row["attack"]] = row["count"]

    return summary



