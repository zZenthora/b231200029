import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        event_data = {
            "event_type": event.event_type,
            "is_directory": event.is_directory,
            "src_path": event.src_path
        }

        try:
            with open("/home/ubuntu/bsm/logs/changes.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(event_data)

        with open("/home/ubuntu/bsm/logs/changes.json", "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    path = "/home/ubuntu/bsm/test"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
