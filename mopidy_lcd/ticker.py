import threading
import time


class Ticker(threading.Thread):

    def __init__(self, actor, interval):
        threading.Thread.__init__(self)
        self.actor = actor
        self.interval = interval

    def run(self):
        while True:
            self.actor.tell({Ticker.TICK: True})
            time.sleep(self.interval)

    TICK = 'tick'
