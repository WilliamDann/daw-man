# Loop.py
# Loop Audio
import soundfile as sf
import queue
import numpy as np

class Loop():
    def __init__(self, key, samplerate=48000, channels=1, device=1, record=False, playback=True):
        # recorded data
        self.key  = key
        self.data = np.array([])
        self.idx  = 0

        # state information
        self.record   = record
        self.playback = playback
        self.loop     = True
        
        # recording params
        self.samplerate = samplerate
        self.channels   = channels
        self.device     = device

    # Dump to file
    def dump(self, filename=None):
        if not filename:
            filename = self.key + "_dump.wav"

        with sf.SoundFile(filename, mode='x', samplerate=self.samplerate, channels=self.channels) as file:
            for chunk in self.data:
                file.write(chunk)

    def __str__(self):
        string = ""
        if self.record:
            string += "\N{Large Red Circle} "
        if self.playback:
            string += "\u25B8 "
        string += self.key

        return string