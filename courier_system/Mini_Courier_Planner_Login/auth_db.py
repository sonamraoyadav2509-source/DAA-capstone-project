
import hashlib
import hmac
import secrets
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "courier_admin",
    "password": "CourierApp@2026",
    "database": "mini_courier_db",
    "port": 3306
}

DEFAULT_USER_ID = "admin"
DEFAULT_PASSWORD = "Courier@123"


def _get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        raise RuntimeError(f"MySQL Connection Failed: {exc}")


def _hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 200000
    )
    return salt.hex(), digest.hex()


def init_db():
    con = _get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(50) PRIMARY KEY,
                salt VARCHAR(32),
                password_hash VARCHAR(64) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = 'users'
            AND COLUMN_NAME = 'full_name'
        """, (DB_CONFIG["database"],))

        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN full_name VARCHAR(100)"
            )

        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = %s",
            (DEFAULT_USER_ID,)
        )

        if cursor.fetchone() is None:
            salt, digest = _hash_password(DEFAULT_PASSWORD)
            cursor.execute("""
                INSERT INTO users
                (user_id, salt, password_hash, full_name)
                VALUES (%s, %s, %s, %s)
            """, (DEFAULT_USER_ID, salt, digest, "Administrator"))

        con.commit()
        cursor.close()
    finally:
        con.close()


def register_user(full_name, user_id, password):
    full_name = full_name.strip()
    user_id = user_id.strip()

    if not full_name or not user_id:
        raise ValueError("Name and User ID are required.")

    if len(user_id) < 4:
        raise ValueError("User ID must be at least 4 characters.")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")

    salt, digest = _hash_password(password)

    con = _get_connection()
    try:
        cursor = con.cursor()

        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = %s",
            (user_id,)
        )

        if cursor.fetchone():
            raise ValueError("User ID already exists.")

        cursor.execute("""
            INSERT INTO users
            (user_id, salt, password_hash, full_name)
            VALUES (%s, %s, %s, %s)
        """, (user_id, salt, digest, full_name))

        con.commit()
        cursor.close()

    except Error as exc:
        if exc.errno == 1062:
            raise ValueError("User ID already exists.")
        raise
    finally:
        con.close()


def verify_login(user_id, password):
    con = _get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("""
            SELECT salt, password_hash
            FROM users WHERE user_id = %s
        """, (user_id.strip(),))

        row = cursor.fetchone()
        cursor.close()
    finally:
        con.close()

    if not row or not row[0]:
        return False

    _, candidate = _hash_password(
        password, bytes.fromhex(row[0])
    )

    return hmac.compare_digest(candidate, row[1])


def change_password(user_id, new_password):
    if len(new_password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    salt, digest = _hash_password(new_password)

    con = _get_connection()
    try:
        cursor = con.cursor()

        cursor.execute("""
            UPDATE users
            SET salt = %s, password_hash = %s
            WHERE user_id = %s
        """, (salt, digest, user_id.strip()))

        if cursor.rowcount == 0:
            raise ValueError("User ID not found.")

        con.commit()
        cursor.close()
    finally:
        con.close()
