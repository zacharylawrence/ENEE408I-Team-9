#!/usr/bin/env python
# encoding: utf-8
"""
Drive the Robot
"""

from arduino import Arduino

def main():
  arduino = Arduino()

  # arduino.blink_led()
  # arduino.set_motors(0.25, -0.25)
  print("Ping: " + str(arduino.get_ping()))
  # arduino.get_ping()

  arduino.shutdown()

if __name__ == '__main__':
  main()
