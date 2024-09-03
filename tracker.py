import watchdog.events
import watchdog.observers
import time
import math as m

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['success.txt'],
                                                             ignore_directories=True, case_sensitive=False)
        self.completed = False

    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)

    # Event is created, you can process it now

    def on_modified(self, event):
        print("OCR Done! % s." % event.src_path)
        # Event is modified, you can process it now
        self.completed = True


def look_for_completion(location):
    src_path = location
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    print("OCR started. Waiting for completion...")
    try:
        while True:
            time.sleep(1)  # Increase the sleep time for main machine
            if event_handler.completed:
                observer.stop()
                break

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
