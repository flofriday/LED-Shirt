import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
ROWS = 8
COLS = 32
NUM_LEDS = ROWS * COLS
BRIGHTNESS = 0.1


@asm_pio(
    sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24
)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]


# Create the StateMachine with the ws2812 program, outputting on Pin(0).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(0))
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
pixel_array = array.array("I", [0 for _ in range(NUM_LEDS)])


############################################
# Functions for RGB Coloring
############################################


def update_pixel():  # dimming colors and updating state machine (state_mach)
    dimmer_array = array.array("I", [0 for _ in range(NUM_LEDS)])
    for ii, cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * BRIGHTNESS)
        g = int(((cc >> 16) & 0xFF) * BRIGHTNESS)
        b = int((cc & 0xFF) * BRIGHTNESS)
        dimmer_array[ii] = (g << 16) + (r << 8) + b
    sm.put(dimmer_array, 8)  # update the state machine with new colors


def clear_all():
    set_all_color((0, 0, 0))


def set_all_color(color):
    for ii in range(len(pixel_array)):
        pixel_array[ii] = (color[1] << 16) + (color[0] << 8) + color[2]


def set_one(pos, color):
    # This function does some weired math because of the orientation of the
    # matrix.
    x, y = pos

    # Don't draw pixels outside the bounds
    if x < 0 or y < 0 or x >= COLS or y >= ROWS:
        return

    # Correct for "Snake" LED layout on the matrix
    if x % 2 == 1:
        y = ROWS - 1 - y

    # Calculate the index in the chain from the position
    index = (255 - 7) - (8 * x) + y
    # print(pos)
    # print(index)
    pixel_array[index] = (color[1] << 16) + (color[0] << 8) + color[2]
