import sqlite3
import hashlib
import os

def create_database_if_not_exists(db_path):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS signatures (hash TEXT PRIMARY KEY)')
        conn.commit()
        conn.close()
        print(f"Database created at {db_path}")

def load_signature_db(db_path):
    create_database_if_not_exists(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    signatures = set(row[0] for row in cursor.execute('SELECT hash FROM signatures'))
    conn.close()
    return signatures

def scan_file(filename, signature_db):
    with open(filename, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash not in signature_db
