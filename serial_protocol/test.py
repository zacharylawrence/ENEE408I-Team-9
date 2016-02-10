import serial
import time
import struct

def establishConnection():
  # Define Constants
  SERIAL_DEVICE = "/dev/tty.usbmodem1411"

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

  message = bytearray(9)

  # Write OpCode
  message[0] = struct.pack("B", 1)

  # Write Left Motor Direction
  if (left >= 0):
    message[1] = struct.pack("B", 0)
  else:
    message[1] = struct.pack("B", 1)

  # Write Left Motor Speed
  message[2] = struct.pack("B", 255)

  # Write Right Motor Direction
  if (right >= 0):
    message[3] = struct.pack("B", 0)
  else:
    message[3] = struct.pack("B", 1)

  # Write Right Motor Speed
  message[4] = struct.pack("B", 130)

  message[5] = struct.pack("B", 0)

  print("Sending: " + hexDump(message))
  ser.write(message)

  print("Response: " + ser.read(3))

def hexDump(dump):
  return ":".join("{:02x}".format(c) for c in dump)

if __name__ == '__main__':
  ser = establishConnection()
  # sendDrive(ser, -1.0, -1.0)
  # time.sleep(5)
  sendDrive(ser, 1.0, 1.0)
  # time.sleep(5)
  # sendDrive(ser, 0.0, 0.0)
