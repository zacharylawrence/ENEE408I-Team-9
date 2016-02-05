import serial
import time

# Define Constants
SERIAL_DEVICE = "/dev/tty.usbmodem1421"

# Establish Connection
ser = serial.Serial(SERIAL_DEVICE, 9600)
time.sleep(2)
print("Connection Established");

# Send Data to Pi
ser.write('h')
time.sleep(5);
ser.write('l')
