import serial
import time

# Define Constants
SERIAL_DEVICE = "/dev/ttyACM0"

# Establish Connection
ser = serial.Serial(SERIAL_DEVICE, 9600)
time.sleep(2)
print("Connection Established");

# Send Data to Pi
ser.write('h')
time.sleep(5);
ser.write('l')
