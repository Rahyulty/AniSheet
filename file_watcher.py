import subprocess, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, sys

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.proc = None
        self.run_app()

    def run_app(self):
        if self.proc:
            self.proc.kill()
        self.proc = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print("🔁 Reloading...")
            self.run_app()

if __name__ == "__main__":
    script = "main.py"  # change to your file name
    event_handler = ReloadHandler(script)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

