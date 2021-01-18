from threading import Thread
from queue     import Queue
from numpy     import append
import sounddevice as sd

# Thread for recording
class RecordThread(Thread):
    def __init__(self, samplerate=48000, device=1, channels=1):
        Thread.__init__(self)

        # record info
        self.samplerate = samplerate
        self.device     = device
        self.channels   = channels

        # state info
        self.record = True
        self.loop   = True

        # Data
        self.locations = []
        self.data      = Queue()
    
    # handle data from audio device
    def handleData(self, indata, frames, time, status):
        if not self.record:
            return
        
        if status:
            print(status)
        self.data.put(indata.copy())

    # Thread run
    def run(self):
        with sd.InputStream(samplerate=self.samplerate, device=self.device, channels=self.channels, callback=self.handleData):
            while self.loop:
                data = self.data.get()
                for location in self.locations:
                    location.data = append(location.data, data)

    def stop(self):
        self.loop = False