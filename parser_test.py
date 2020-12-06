import threading
import time
class ParserClass(threading.Thread):
    def __init__(self, *args, **kwargs): 
        super(ParserClass, self).__init__(*args, **kwargs) 
        self._stop = threading.Event() 

    def stop(self): 
        self._stop.set() 
    def run(self):
        while True:
            time.sleep(1)
            print("Next")

a = ParserClass()
a.start()
a.join(5)
print("Shutting down")
a.stop()
print("Waiting to finish")
a.join()
print("Done!")