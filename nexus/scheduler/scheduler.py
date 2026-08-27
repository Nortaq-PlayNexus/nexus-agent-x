"""Scheduler — one-time, recurring, event-triggered (ULTRA §37)."""
import threading, time
from datetime import datetime

class Scheduler:
    def __init__(self, bus=None):
        self.bus=bus
        self.jobs=[]

    def every(self, seconds: int, fn, *a, **kw):
        def loop():
            while True:
                time.sleep(seconds)
                try: fn(*a,**kw)
                except Exception: pass
        t=threading.Thread(target=loop, daemon=True)
        t.start()
        self.jobs.append(t)
        return t

    def at(self, when: datetime, fn, *a, **kw):
        delay=(when - datetime.utcnow()).total_seconds()
        if delay<0: delay=0
        def one():
            time.sleep(delay)
            fn(*a,**kw)
        threading.Thread(target=one, daemon=True).start()

    def on_event(self, event_type: str, fn):
        if self.bus:
            self.bus.on(event_type, lambda evt: fn(evt))
