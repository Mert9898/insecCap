import sqlite3
import os

def create_database(db_path):
    # Ensure the file does not exist
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create a new database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE signatures (hash TEXT PRIMARY KEY)')
    conn.commit()
    conn.close()
    print(f"Database successfully created at {db_path}")

if __name__ == "__main__":
    create_database('virus_definitions.db')
