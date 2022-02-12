import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess


class ScanPyFiles:
    def __init__(self, process: subprocess, cmd: str):
        self.process = process
        self.event_handler = PatternMatchingEventHandler(
            patterns=["*.py"], ignore_patterns=[], ignore_directories=True
        )
        self.event_handler.on_any_event = self.on_any_event
        self.observer = Observer()
        self.observer.schedule(self.event_handler, ".", recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.process.pid))
        self.process = subprocess.Popen(cmd, shell=True)
        print("Server Restarted")

    def stop(self):
        self.observer.stop()
        self.observer.join()


cmd = "python3 run_app.py"
process = subprocess.Popen(cmd, shell=True)
scan_py_files = ScanPyFiles(process, cmd)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Ouch !!! Keyboard interrupt received.")

scan_py_files.stop()