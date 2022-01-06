import meshtastic
import time

interface = meshtastic.SerialInterface(devPath='COM4') # By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface.sendText("hello mesh") # or sendData to send binary data, see documentations for other options.

counter = 0

while True:
    try:
        msg = f"test: {str(counter)}"
        print(msg)
        interface.sendText(msg)
        counter += 1
        time.sleep(5)
    except KeyboardInterrupt:
        break

interface.close()