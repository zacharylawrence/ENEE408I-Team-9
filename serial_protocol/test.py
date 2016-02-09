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

  ser.write('1')
  #ser.write('0' if left >= 0 else '1')
  #ser.write(struct.pack("B", abs(left) * 255))
  #ser.write('0' if right >= 0 else '1')
  #ser.write(struct.pack("B", abs(right) * 255))

  ser.write('0')
  ser.write(bytes(255))
  ser.write('0')
  ser.write(bytes(255))

  ser.write('0')
  ser.write('0')
  ser.write('0')
  ser.write('0')

  print('test')

if __name__ == '__main__':
  ser = establishConnection()
  sendDrive(ser, -1.0, -1.0)
  time.sleep(5)
  sendDrive(ser, 1.0, 1.0)
  time.sleep(5)
  sendDrive(ser, 0.0, 0.0)
