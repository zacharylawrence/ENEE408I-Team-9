#!/usr/bin/env python
# encoding: utf-8
"""
Drive the Robot
"""

from arduino import Arduino

def main():
  arduino = Arduino()

  arduino.blink_led()
  arduino.set_motor(0, 0)

  arduino.shutdown()

if __name__ == '__main__':
  main()
