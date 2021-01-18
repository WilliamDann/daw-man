import queue

import sounddevice as sd
import soundfile as sf
import numpy

q = queue.Queue()

samplerate = 48000
channels   = 1
device     = 1
filename    = "test.wav"

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata.copy())


try:
    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=channels) as file:
        with sd.InputStream(samplerate=samplerate, device=device, channels=channels, callback=callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(filename))
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))