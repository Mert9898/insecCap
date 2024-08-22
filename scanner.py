import sqlite3
import hashlib
import os
import shutil
import requests

# Constants
QUARANTINE_DIR = "quarantine"
SIGNATURE_UPDATE_URL = "https://example.com/signature_updates.txt"  # Update with the actual URL
HEURISTIC_PATTERNS = ["eval(", "exec(", "subprocess", "import os"]  # Example heuristic patterns

def update_signature_db(db_path):
    try:
        response = requests.get(SIGNATURE_UPDATE_URL)
        if response.status_code == 200:
            signatures = response.text.splitlines()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            for signature in signatures:
                cursor.execute('INSERT OR IGNORE INTO signatures (hash) VALUES (?)', (signature,))
            conn.commit()
            conn.close()
            print("Signature database updated successfully.")
        else:
            print("Failed to update signature database. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error updating signature database:", e)

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

def move_to_quarantine(filename):
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    basename = os.path.basename(filename)
    quarantine_path = os.path.join(QUARANTINE_DIR, basename)
    shutil.move(filename, quarantine_path)
    print(f"File {filename} moved to quarantine.")

def scan_file(filename, signature_db):
    """Scans the file against the signature database and moves to quarantine if infected."""
    with open(filename, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    if file_hash in signature_db:
        move_to_quarantine(filename)
        return False  # Infected
    return True  # Clean

def heuristic_analysis(filename):
    """Performs heuristic analysis to detect suspicious patterns."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
            for pattern in HEURISTIC_PATTERNS:
                if pattern in content:
                    move_to_quarantine(filename)
                    print(f"Heuristic analysis detected suspicious pattern in {filename}.")
                    return False  # Suspicious
        return True  # Clean
    except Exception as e:
        print(f"Error during heuristic analysis of {filename}: {e}")
        return True  # Assuming clean if an error occurs

def scan_with_heuristics(filename, signature_db):
    """Combines signature-based scanning with heuristic analysis."""
    if scan_file(filename, signature_db):
        return heuristic_analysis(filename)
    return False  # Infected by signature detection

