import requests
import threading


class Worker(threading.Thread):

    def __init__(self, url, auth, callback):
        super(Worker, self).__init__()
        self.url = url
        self.auth = auth
        self.on_data = callback
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        try:
            r = requests.get(self.url, auth=self.auth, stream=True, timeout=(3.05, 30))
            for line in r.iter_lines():
                if self.stopped():
                    break
                elif line:
                    self.on_data(line)
            self.stop()
        except:
            self.stop()
            raise
