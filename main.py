from RecordThread import *
from Loop         import *
from msvcrt       import getch

import soundfile as sf

# Show UI
def showUI():
    print('\033c') # Clear console
    print(title)
    for loop in recordThread.locations:
        print(loop, end=", ")
    print()
    if setRecord:
        print("Press to record...")

# check if a loop's key exists
def getKeyLoop(key):
    for loop in recordThread.locations:
        if loop.key == key:
            return loop
    return None

title = "DAW-Man"
with open('title.txt', 'r') as file:
    title = file.read()

setRecord = False
infoMode  = False

# Start threads
recordThread = RecordThread()
recordThread.start()
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
    loop = getKeyLoop(key)
    if loop is not None:
        if setRecord:
            loop.record = not loop.record
        elif infoMode:
            print("size: " + str(loop.data.size))
            loop.dump()
            getch()
        else:
            loop.playback = not loop.playback
    else:
        recordThread.locations.append(Loop(key, record=setRecord))

# Exit threads
recordThread.stop()