import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio
import math
import random

import matrix
import text


def millis():
    return time.ticks_ms()


# Color based on RGB (R,G,B)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
grey = (100, 100, 100)
black = (0, 0, 0)
pink = (255, 20, 147)

colors = [red, green, blue, pink, white]


led = Pin(25, Pin.OUT)  # 14 number in is Output
brightness_button = Pin(13, Pin.IN)  # 13 number pin is input
brightness_button_block = False

# Yes I hacked a special mode into the brightness because I hand no time
# to solder another button... SUE ME!
brightness_levels = [0.05, 0.1, 0.25, 0.50, 0.75, 0.50]  # 0.75, 1.0]
brightness_index = len(brightness_levels) - 1

loop_special = True


def ani_science():
    text.fg_color = white
    text.bg_color = red
    return text.scroll("Science", 0.08)


def ani_hi():
    return text.display("Hi", 0.7)


def ani_do_more():
    text.fg_color = random.choice(colors)
    return text.flash("Do more", 1)


def ani_all_in():
    text.fg_color = random.choice(colors)
    return text.flash("All in!", 1.0)


def ani_last_night():
    text.fg_color = random.choice(colors)
    return text.scroll("Letzte Nacht in Freiheit!", 0.1)


def ani_gemma():
    text.fg_color = pink
    text.bg_color = grey
    return text.flash("Gemma Paul!", 0.5)


def ani_fucked():
    text.fg_color = random.choice(colors)
    return text.scroll(
        "Do more science, just really weird, fucked-up shit, stuff where even you are like man, I should not have done that...do that!",
        0.08,
    )


def ani_special():
    text.fg_color = pink
    text.bg_color = black
    return text.scroll(
        "Nobody exists on purpose. Nobody belongs anywhere. We are all going to die. Come play hardstyle.",
        0.08,
    )


animations = [
    # ani_hi,
    ani_do_more,
    ani_science,
    ani_all_in,
    ani_gemma,
    ani_last_night,
    ani_fucked,
    # ani_lena,
]
animation_index = 0
current_animation = ani_special()

# Here we read the buttons and handle them accordingly.
# There is no debounce algorithm, probably because the eventhandlers are so
# slow that the are a "natural" debounce. So yeah I won't implement one
# if it does work.
def check_buttons():
    global brightness_index
    global brightness_button_block
    global loop_special
    global current_animation

    logic_state = brightness_button.value()
    if logic_state and not brightness_button_block:  # if push_button pressed
        # End the startloop
        loop_special = False
        current_animation = animations[animation_index]()

        brightness_button_block = True
        led.value(1)  # led will turn ON
        brightness_index = (brightness_index + 1) % len(brightness_levels)
        matrix.BRIGHTNESS = brightness_levels[brightness_index]
        matrix.update_pixel()
    elif not logic_state:  # if push_button not pressed
        led.value(0)  # led will turn OFF
        brightness_button_block = False


def update_display():
    global animation_index
    global current_animation
    global timestamp

    finished = current_animation()
    if finished:
        if loop_special:
            current_animation = ani_special()
            return

        text.reset_color()
        animation_index = (animation_index + 1) % len(animations)
        current_animation = animations[animation_index]()


# This is the main loop of the firmware.
# This loop runs constantly and all functions that are called from here are
# designed to be not blocking (no time.sleep here) and will return as quickly
# as possible.
while True:
    check_buttons()
    update_display()


# current = 0
# while True:
#     for y in range(matrix.ROWS):
#         for x in range(matrix.COLS):
#             matrix.clear_all()
#             matrix.set_one((x, y), (255, 0, 0))
#             matrix.update_pixel()
#             time.sleep(0.1)

# current = 0
# while True:
#     matrix.clear_all()
#     for y in range(matrix.ROWS):
#         for x in range(matrix.COLS):
#             matrix.set_one((x, y), (255, 0, 0))

#         matrix.update_pixel()
#         time.sleep(0.25)


# while True:
#     current = ""
#     for c in "Lena":
#         current = current + c
#         matrix.clear_all()
#         text.display(current)
#         matrix.update_pixel()
#         time.sleep(0.7)

#     current = ""
#     for c in "...":
#         current = current + c
#         matrix.clear_all()
#         text.display(current)
#         matrix.update_pixel()
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


# text.scroll("We want happy hardstyle!", 0.05)
