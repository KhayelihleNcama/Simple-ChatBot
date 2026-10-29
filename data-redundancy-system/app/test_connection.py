import hashlib
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Open a connection using the settings stored in .env."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "dedup_system"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )


def make_fingerprint(name, email):
    """SHA-256 hash of the key fields. (Real normalization comes in Step 4.)"""
    return hashlib.sha256(f"{name}|{email}".encode("utf-8")).hexdigest()

