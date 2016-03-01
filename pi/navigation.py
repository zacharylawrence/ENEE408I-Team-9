#!/usr/bin/env python
# encoding: utf-8
"""
Control Navigation Features
"""

class Navigation():
  def __init__(self):
    # TODO
    return None

  # Gets the pixy block with the largest size in the frame
  def get_pixy_block(self, pixy_blocks):
    if (len(pixy_blocks) == 0):
      return None

    max_block_index = 0
    max_block_size = blocks[0]["width"] * blocks[0]["height"]

    for block_index in range(len(blocks)):
      block = blocks[block_index]
      size = block["width"] * block["height"]
      if (size > max_block_size):
        max_block_index = block_index
        max_block_size = size

    return pixy_blocks[max_block_index]

  def with_pixy(self, pixy_blocks):
    block = self.get_pixy_block(pixy_blocks)
    if (block == None):
      print("Could not get pixy data")
      return (0.0, 0.0)

    print("x:" + str(block["x"]))
    if (block["x"] < 100):
      print("Go left")
      return(-0.1, 0.1)
    elif(block["x"] > 200):
      print("Go right")
      return(0.1, -0.1)
    else:
      return(0.0, 0.0)

  # Return left/right motor speeds
  def hold_ping(self, distance):
    if (distance == None):
      return (0, 0)

    if (distance < 20):
      return (-0.1, -0.1)
    elif (distance > 20):
      return (0.1, 0.1)
    else:
      return (0, 0)
