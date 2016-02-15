#!/usr/bin/env python
# encoding: utf-8
"""
Control All Arduino Functions
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

class Arduino():
  # Define Pin Constants
  _MOTOR1 = 3
  _MOTOR1_DIR_A = 2
  _MOTOR1_DIR_B = 4

  _MOTOR2 = 6
  _MOTOR2_DIR_A = 7
  _MOTOR2_DIR_B = 8

  _LED = 13


  def __init__(self):
    # Instantiate the pymata_core API
    self.board = PyMata3()

    # set the pin mode
    self.board.set_pin_mode(self._MOTOR1, Constants.PWM)
    self.board.set_pin_mode(self._MOTOR1_DIR_A, Constants.OUTPUT)
    self.board.set_pin_mode(self._MOTOR1_DIR_B, Constants.OUTPUT)

    self.board.set_pin_mode(self._MOTOR2, Constants.PWM)
    self.board.set_pin_mode(self._MOTOR2_DIR_A, Constants.OUTPUT)
    self.board.set_pin_mode(self._MOTOR2_DIR_B, Constants.OUTPUT)

    self.board.set_pin_mode(self._LED, Constants.OUTPUT)

  def set_motor(selft, motor1, motor2):
    if (motor1 < -1 or motor1 > 1 or motor2 < -1 or motor2 > 1):
      raise ValueError("set_motor called with (motor1=" + str(motor1) + ") and (motor2=" + str(motor2) + ")")

    # Set motor1 direction
    self.board.digital_write(_MOTOR1_DIR_A, 0 if (motor1 < 0) else 1)
    self.board.digital_write(_MOTOR1_DIR_B, 1 if (motor1 < 0) else 0)

    self.board.digital_write(_MOTOR2_DIR_A, 0 if (motor2 < 0) else 1)
    self.board.digital_write(_MOTOR2_DIR_B, 1 if (motor2 < 0) else 0)


  def blink_led(self):
    self.board.digital_write(13, 1)
    self.board.sleep(2)
    self.board.digital_write(13, 0)
    self.board.sleep(2)
    self.board.digital_write(13, 1)
    self.board.sleep(2)
    self.board.digital_write(13, 0)
    self.board.sleep(2)

  def shutdown(self):
    # Reset the board and exit
    self.board.shutdown()
