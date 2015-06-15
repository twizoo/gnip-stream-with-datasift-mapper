import time
from worker import Worker


class StreamConsumer(object):

    def __init__(self, callback, url, auth):
        self.callback = callback
        self.url = url
        self.auth = auth

    def start(self):
        self.worker = Worker(self.url, self.auth, self.callback)
        self.worker.start()
        while not self.worker.stopped():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print "\n"
                print "Exiting..."
                self.worker.stop()
                self.worker.join()
                raise
            except:
                raise
