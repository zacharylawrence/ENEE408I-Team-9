from pyfirmata import Arduino, util
import time

board = Arduino('/dev/tty.usbmodem1421')

board.digital[13].write(1)
print("high")
time.sleep(5)
board.digital[13].write(0)
print("low")
time.sleep(5)
board.digital[13].write(1)
print("high")
