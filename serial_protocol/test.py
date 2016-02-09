import serial
import time
import binascii
import struct

def establishConnection():
  # Define Constants
  SERIAL_DEVICE = "/dev/ttyACM0"

  # Establish Connection
  ser = serial.Serial(SERIAL_DEVICE, 9600)
  time.sleep(2)
  print("Connection Established")

  return ser

# Each motor speed is a float from -1.0 to 1.0
def sendDrive(ser, left, right):
  if(left < -1 or left > 1 or right < -1 or right > 1):
    print("Incorrectly formated drive command!")
    return;

  # Write OpCode
  ser.write('1')

  # Write Left Motor Direction
  if (left >= 0):
    ser.write(bytes(0))
  else:
    ser.write(bytes(1))

  # Write Left Motor Speed
  ser.write(bytes(abs(left * 255)))

  # Write Right Motor Direction
  if (right >= 0):
    ser.write(bytes(0))
  else:
    ser.write(bytes(1))

  # Write Right Motor Speed
  ser.write(bytes(abs(right * 255)))

  # Pad message to 9 bytes
  ser.write(bytes(0))
  ser.write(bytes(0))
  ser.write(bytes(0))
  ser.write(bytes(0))

  print('Test')

if __name__ == '__main__':
  ser = establishConnection()
  sendDrive(ser, -1.0, -1.0)
  time.sleep(5)
  sendDrive(ser, 1.0, 1.0)
  time.sleep(5)
  sendDrive(ser, 0.0, 0.0)
