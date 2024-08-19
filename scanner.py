import hashlib

def get_file_hash(file_path):
    """Compute the hash of a file."""
    hash_func = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def scan_file(file_path, signature_db):
    """Scan a file against a database of known signatures."""
    file_hash = get_file_hash(file_path)
    return file_hash in signature_db
