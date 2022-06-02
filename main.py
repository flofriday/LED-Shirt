import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio
import math

import matrix
import text


# Color based on RGB (R,G,B)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


# current = 0
# while True:
#     for y in range(matrix.ROWS):
#         for x in range(matrix.COLS):
#             matrix.clear_all()
#             matrix.set_one((x, y), (255, 0, 0))
#             matrix.updatePixel()
#             time.sleep(0.1)

# current = 0
# while True:
#     matrix.clear_all()
#     for y in range(matrix.ROWS):
#         for x in range(matrix.COLS):
#             matrix.set_one((x, y), (255, 0, 0))

#         matrix.updatePixel()
#         time.sleep(0.25)


# while True:
#     current = ""
#     for c in "Lena":
#         current = current + c
#         matrix.clear_all()
#         text.display(current)
#         matrix.updatePixel()
#         time.sleep(0.7)

#     current = ""
#     for c in "...":
#         current = current + c
#         matrix.clear_all()
#         text.display(current)
#         matrix.updatePixel()
#         time.sleep(0.33)

# while True:
#     current = ""
#     for c in "Lennna":
#         current = current + c
#         text.display(current)
#         time.sleep(0.7)

#     current = ""
#     for c in "...":
#         current = current + c
#         text.display(current)
#         time.sleep(0.33)


text.scroll("We want happy hardstyle!", 0.05)
