from LoopManager import *
from Loop        import *
from msvcrt      import getch

import soundfile as sf

# Show UI
def showUI():
    print('\033c') # Clear console
    print(title)
    for loop in loopManager.loops:
        print(loop, end=", ")
    print()
    if setRecord:
        print("Press to record...")

title = "DAW-Man"
with open('title.txt', 'r') as file:
    title = file.read()

setRecord = False
infoMode  = False

# Start threads
loopManager = LoopManager([], 1024)
loopManager.start()
while True:
    showUI()

    # Get key input
    key = getch()
    if key == b'\x03':
        break
    if key == b'\r':
        setRecord = not setRecord
        continue
    if key == b'?':
        infoMode = not infoMode
        continue
    key = key.decode('utf-8')

    # Set record/playback flags
    loop = loopManager.getLoopByKey(key)
    if loop is not None:
        if setRecord:
            loop.record = not loop.record
        elif infoMode:
            print("size: " + str(len(loop.data)))
            loop.dump()
            getch()
        else:
            loop.playback = not loop.playback
    else:
        loopManager.loops.append(Loop((loopManager.blocksize, loopManager.channels), key, record=setRecord))

# Exit threads
loopManager.stop()