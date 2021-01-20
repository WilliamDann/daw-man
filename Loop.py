# Loop.py
# Loop Audio
import soundfile as sf
import queue
import numpy as np

class Loop():
    def __init__(self, shape, key, record=False, playback=False):
        # data
        self.key  = key
        self.data = []

        # state information
        self.record   = record
        self.playback = playback
        self.idx      = 0

    # Get next audio frame
    def getFrame(self):
        frame = self.data[self.idx]
        self.idx += 1

        if self.idx >= len(self.data):
            self.idx = 0

        return frame

    # Dump to file
    #def dump(self, filename=None):
    #    if not filename:
    #        filename = self.key + "_dump.wav"
    #
    #    with sf.SoundFile(filename, mode='x', samplerate=self.samplerate, channels=1) as file:
    #        for chunk in self.data:
    #            file.write(chunk)

    def __str__(self):
        string = ""
        if self.record:
            string += "\N{Large Red Circle} "
        if self.playback:
            string += "\u25B8 "
        string += self.key

        return string