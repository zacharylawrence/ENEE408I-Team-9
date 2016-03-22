#!/usr/bin/env python
# encoding: utf-8
"""
Control Pixy Features
"""

from collections import deque

class Pixy():
  def __init__(self, max_queue_size=3):
    self.max_queue_size = max_queue_size
    self.blocks_queue = deque()

  # Gets the pixy block with the largest size in the frame
  def get_pixy_block(self, pixy_blocks):
    if (len(pixy_blocks) == 0):
      return None

    max_block_index = 0
    max_block_size = pixy_blocks[0]["width"] * pixy_blocks[0]["height"]

    for block_index in range(len(pixy_blocks)):
      block = pixy_blocks[block_index]
      size = block["width"] * block["height"]
      if (size > max_block_size):
        max_block_index = block_index
        max_block_size = size

    return pixy_blocks[max_block_index]

  def get_pixy_block_x_average(self, pixy_blocks):
    self.blocks_queue.append(self.get_pixy_block(pixy_blocks))  # add our new block
    if (len(self.blocks_queue) > self.max_queue_size):
      self.blocks_queue.popleft()  # remove our old block

    block_count = 0
    block_x_average = 0;
    for block in self.blocks_queue:
      if (block != None):
        block_x_average += block["x"]
        block_count += 1

    if (block_count != 0):
      return block_x_average / block_count
    else:
      return None
