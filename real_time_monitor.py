from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scanner import scan_file, move_to_quarantine, heuristic_analysis

class FileHandler(FileSystemEventHandler):
    def __init__(self, signature_db):
        self.signature_db = signature_db

    def on_created(self, event):
        if not event.is_directory:
            if not scan_file(event.src_path, self.signature_db):
                print(f"Alert: File {event.src_path} is infected!")
                move_to_quarantine(event.src_path)  # Example usage
            else:
                heuristic_analysis(event.src_path)  # Example heuristic check

def start_real_time_monitor(signature_db, path='.'):
    """Start monitoring a directory for new files."""
    observer = Observer()
    observer.schedule(FileHandler(signature_db), path=path, recursive=False)
    observer.start()
