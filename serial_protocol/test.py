import serial
import time
import binascii
import struct

def establishConnection():
  # Define Constants
  SERIAL_DEVICE = "/dev/tty.usbmodem1421"

  # Establish Connection
  ser = serial.Serial(SERIAL_DEVICE, 9600)
  time.sleep(2)
  print("Connection Established")

# Each motor speed is a float from -1.0 to 1.0
def sendDrive(left, right):
  if(left < -1 or left > 1 or right < -1 or right > 1):
    print("Incorrectly formated drive command!")
    return;

  message = bytearray(9)

  message[0] = 1
  message[1] = 0 if left >= 0 else 1
  message[2] = struct.pack("B", abs(left) * 255)
  message[3] = 0 if right >= 0 else 1
  message[4] = struct.pack("B", abs(right) * 255)

  print binascii.hexlify(message)
  # ser.write(message)

if __name__ == '__main__':
  # establishConnection()
  sendDrive(-1.0, -1.0)
  time.sleep(5)
  sendDrive(1.0, 1.0)
  time.sleep(5)
  sendDrive(0.0, 0.0)
