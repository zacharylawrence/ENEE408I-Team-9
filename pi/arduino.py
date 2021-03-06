#!/usr/bin/env python
# encoding: utf-8
"""
Control All Arduino Functions
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

import constants

class Arduino():
  # Define Pin Constants
  # SPI (for pixy) uses pins 10-13
  _MOTOR1 = 3
  _MOTOR1_DIR_A = 2
  _MOTOR1_DIR_B = 4

  _MOTOR2 = 6
  _MOTOR2_DIR_A = 7
  _MOTOR2_DIR_B = 8

  # Note: ping sensor shouldn't have to be PWM
  _PING = 5

  _SERVO = 9

  # Analog Pins
  _IR_LEFT = 0
  _IR_MID = 1
  _IR_RIGHT = 2


  def __init__(self):
    # Instantiate the pymata_core API
    self.board = PyMata3(sleep_tune=0)

    # Set the pin modes
    self.board.set_pin_mode(self._MOTOR1, Constants.PWM)
    self.board.set_pin_mode(self._MOTOR1_DIR_A, Constants.OUTPUT)
    self.board.set_pin_mode(self._MOTOR1_DIR_B, Constants.OUTPUT)

    self.board.set_pin_mode(self._MOTOR2, Constants.PWM)
    self.board.set_pin_mode(self._MOTOR2_DIR_A, Constants.OUTPUT)
    self.board.set_pin_mode(self._MOTOR2_DIR_B, Constants.OUTPUT)

    self.board.set_pin_mode(self._IR_LEFT, Constants.INPUT)
    self.board.enable_analog_reporting(self._IR_LEFT)
    self.board.set_pin_mode(self._IR_MID, Constants.INPUT)
    self.board.enable_analog_reporting(self._IR_MID)
    self.board.set_pin_mode(self._IR_RIGHT, Constants.INPUT)
    self.board.enable_analog_reporting(self._IR_RIGHT)

    self.board.sonar_config(self._PING, self._PING)

    self.board.pixy_init(max_blocks=constants.MAX_PIXY_BLOCKS)
    self.board.keep_alive(period=2)

    self.board.servo_config(self._SERVO)

    # Set default state
    self.set_motors(0, 0)
    self.open_claw()

  def set_motors(self, motor1, motor2):
    if (motor1 < -1 or motor1 > 1 or motor2 < -1 or motor2 > 1):
      raise ValueError("set_motor called with (motor1=" + str(motor1) + ") and (motor2=" + str(motor2) + ")")

    # print("Setting Motor 1 to: " + str(motor1))
    # print("Setting Motor 2 to: " + str(motor2))

    # Set motor directions
    self.board.digital_write(self._MOTOR1_DIR_A, 0 if (motor1 < 0) else 1)
    self.board.digital_write(self._MOTOR1_DIR_B, 1 if (motor1 < 0) else 0)

    self.board.digital_write(self._MOTOR2_DIR_A, 1 if (motor2 < 0) else 0)
    self.board.digital_write(self._MOTOR2_DIR_B, 0 if (motor2 < 0) else 1)

    # Set motor speeds
    self.board.analog_write(self._MOTOR1, int(abs(motor1) * 255))
    self.board.analog_write(self._MOTOR2, int(abs(motor2) * 255))

  def set_servo(self, servo):
    self.board.analog_write(self._SERVO, servo)

  def close_claw(self):
    self.board.analog_write(self._SERVO, 100)  # Used to be 75
    self.board.sleep(constants.CLOSE_CLAW_PAUSE)

  def open_claw(self):
    self.board.analog_write(self._SERVO, 150)
    self.board.sleep(constants.OPEN_CLAW_PAUSE)

  # Get the ping sensor's distance in cm
  def get_ping(self):
    return self.board.sonar_data_retrieve(self._PING)

  # Returns the value from the pixy camera
  def get_pixy_blocks(self):
    blocks = self.board.pixy_get_blocks()
    print(blocks)

    if len(blocks) > 0 and not "signature" in blocks[0]:
        print("Malformed pixy block!!")
        return None

    # for block_index in range(len(blocks)):
      # block = blocks[block_index]
      # print("  block {}: sig: {}  x: {} y: {} width: {} height: {}".format(
          # block_index, block["signature"], block["x"], block["y"], block["width"], block["height"]))

    # print("\n")

    return blocks

  def print_ir(self):
    print(str(self.board.analog_read(self._IR_LEFT)) + "  |  " +
      str(self.board.analog_read(self._IR_MID)) + "  |  " +
      str(self.board.analog_read(self._IR_RIGHT)) + "  |  " +
      str(self.get_ping()))

  def get_ir_left(self):
    return self.board.analog_read(self._IR_LEFT)

  def get_ir_mid(self):
    return self.board.analog_read(self._IR_MID)

  def get_ir_right(self):
    return self.board.analog_read(self._IR_RIGHT)

  def ir_wall(self):
    return (self.get_ir_left() >= constants.IR_WALL_THRESHOLD or
      self.get_ping() <= constants.PING_WALL_THRESHOLD or
      self.get_ir_right() >= constants.IR_WALL_THRESHOLD)

  def ir_wall_target(self):
    return (self.get_ir_left() >= constants.IR_WALL_THRESHOLD or
      self.get_ir_mid() >= constants.IR_WALL_THRESHOLD or
      self.get_ir_right() >= constants.IR_WALL_THRESHOLD)

  def shutdown(self):
    # Reset the board and exit
    self.board.shutdown()
