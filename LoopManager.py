# ThreadManager.py
#   Thread of audio playback & recording into Loops
#
from   threading   import Thread
from   numpy       import append
from   queue       import Queue
import sounddevice as sd

class LoopManager(Thread):
    def __init__(self, loops, blocksize, samplerate=48000, channels=1, device=1):
        Thread.__init__(self)

        # state control
        self.running = True

        # Audio settings
        self.samplerate = samplerate
        self.channels   = channels
        self.device     = device
        self.blocksize  = blocksize

        # data
        self.loops = loops
        self.queue = Queue()

    # sounddevice processing callbacks
    def handleIndata (self, indata,  frames, time, status):
        if status:
            print(status)
        self.queue.put(indata.copy())

    def handleOutdata(self, outdata, frames, time, status):
        if status:
            print(status)

        if (len(self.loops) > 0):
            if (self.loops[0].playback):
                frames = self.loops[0].getFrame()
                outdata[:] = frames
                    
    
    # thread control
    def run(self):
        with sd.InputStream(blocksize=self.blocksize, samplerate=self.samplerate, device=self.device, channels=self.channels, callback=self.handleIndata):
            with sd.OutputStream(blocksize=self.blocksize, samplerate=self.samplerate, channels=self.channels, callback=self.handleOutdata):
                while self.running:
                    
                    data = self.queue.get()
                    for loop in self.loops:
                        if loop.record:
                            loop.data.append(data)

    def stop(self):
        self.running = False

    # data funcs
    def getLoopByKey(self, key):
        for loop in self.loops:
            if loop.key == key:
                return loop
        return None
