import hashlib
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_FILE)

def getConnection():
    """------------Connecting to the database---------------"""
    """---Open a connection using the settings stored in .env.------"""
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError(
            f"DB_PASSWORD is missing. Set it in {ENV_FILE} or in your environment."
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=password,
    )

"""____Normalizing the email by removing white space and making it lowercase_____"""
def normalize_email(email: str) -> str:
    email = (email or "").strip().lower()
    if "@" not in email:
        return email
    local, domain = email.rsplit("@", 1)

    if domain in ("gmail.com", "googlemail.com"):
        local = local.split("+", 1)[0].replace(".", "")
        return f"{local}@gmail.com"
    return f"{local}@{domain}"

def make_fingerprint(name: str, email: str) -> str:
    """SHA-256 hash of the key fields. (Read normalization come in step 4.)"""
    return hashlib.sha256(f"{name}\0{email}".encode("utf-8")).hexdigest()

def insert_if_new(conn, name, email, phone=None) -> bool:
    """True if inserted, False if the fingerprint already existed."""
    email = normalize_email(email)
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO customers (fingerprint, name, email, phone)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (fingerprint) DO NOTHING""",
            (make_fingerprint(name, email), name, email, phone),
        )
        inserted = cur.rowcount == 1
    conn.commit()
    return inserted
if __name__ == "__main__":
    conn = getConnection()
    insert_if_new(conn, "Thandi", "Thandi.M@gmail.com")