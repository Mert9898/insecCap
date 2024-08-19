from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scanner import scan_file

class FileHandler(FileSystemEventHandler):
    def __init__(self, signature_db):
        self.signature_db = signature_db

    def on_created(self, event):
        if not event.is_directory:
            if not scan_file(event.src_path, self.signature_db):
                print(f"Alert: File {event.src_path} is infected!")

def start_real_time_monitor(signature_db, path='.'):
    """Start monitoring a directory for new files."""
    observer = Observer()
    observer.schedule(FileHandler(signature_db), path=path, recursive=False)
    observer.start()
