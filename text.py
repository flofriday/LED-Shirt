import time
import matrix

fg_color = (0, 255, 0)
bg_color = (0, 0, 0)


def reset_color():
    global fg_color
    global bg_color
    fg_color = (0, 255, 0)
    bg_color = (0, 0, 0)


def millis():
    return time.ticks_ms()


# Note: the duration is the duration per frame
def scroll(text, duration):
    text = text.upper()
    length = len(text) - 1 if len(text) > 0 else 0

    for c in text:
        bitmap = char_map[c] if c in char_map else fallback
        length += len(bitmap[0])

    timestamp = millis()

    def callback():
        xpos = matrix.COLS - int((millis() - timestamp) / (duration * 1000))
        matrix.set_all_color(bg_color)

        for c in text:
            bitmap = char_map[c] if c in char_map else fallback

            # Optimize to not draw characters that are out of bounds
            if xpos > matrix.COLS:
                break
            if xpos + len(bitmap[0]) < 0:
                xpos += len(bitmap[0]) + 1
                continue

            for y, _ in enumerate(bitmap):
                for x, _ in enumerate(bitmap[0]):
                    if bitmap[y][x] != ".":
                        matrix.set_one((xpos + x, y), fg_color)

            xpos += len(bitmap[0]) + 1

        matrix.update_pixel()

        if xpos <= 0:
            return True

        return False

    return callback


# Flashes each word for duration
def flash(text, duration):
    words = text.split(" ")
    word_index = 0
    current_animation = display(words[word_index], duration)

    def callback():
        nonlocal current_animation
        nonlocal word_index

        current_done = current_animation()
        if current_done:
            word_index += 1
            if word_index == len(words):
                return True  # We are done flashing all words
            current_animation = display(words[word_index], duration)

        return False

    return callback


def display(text, duration):

    text = text.upper()
    length = len(text) - 1 if len(text) > 0 else 0

    for c in text:
        bitmap = char_map[c] if c in char_map else fallback
        length += len(bitmap[0])

    timestamp = millis()

    def callback():
        xpos = int(matrix.COLS / 2) - int(length / 2)

        matrix.set_all_color(bg_color)

        for c in text:
            bitmap = char_map[c] if c in char_map else fallback
            for y, _ in enumerate(bitmap):
                for x, _ in enumerate(bitmap[0]):
                    if bitmap[y][x] != ".":
                        matrix.set_one((xpos + x, y), fg_color)

            xpos += len(bitmap[0]) + 1

        matrix.update_pixel()

        # Return a bool if the animation is finished
        return millis() > (timestamp + (duration * 1000))

    return callback


char_map = {
    "A": [
        ".##.",
        "#..#",
        "#..#",
        "####",
        "#..#",
        "#..#",
        "#..#",
        "....",
    ],
    "B": [
        "###.",
        "#..#",
        "#..#",
        "###.",
        "#..#",
        "#..#",
        "###.",
        "....",
    ],
    "C": [
        ".##.",
        "#..#",
        "#...",
        "#...",
        "#...",
        "#..#",
        ".##.",
        "....",
    ],
    "D": [
        "###.",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "###.",
        "....",
    ],
    "E": [
        "####",
        "#...",
        "#...",
        "###.",
        "#...",
        "#...",
        "####",
        "....",
    ],
    "F": [
        "####",
        "#...",
        "#...",
        "###.",
        "#...",
        "#...",
        "#...",
        "....",
    ],
    "G": [
        ".###.",
        "#...#",
        "#....",
        "#..##",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ],
    "H": [
        "#..#",
        "#..#",
        "#..#",
        "####",
        "#..#",
        "#..#",
        "#..#",
        "....",
    ],
    "I": [
        "###",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        "###",
        "...",
    ],
    "J": [
        "...#",
        "...#",
        "...#",
        "...#",
        "...#",
        "#..#",
        ".##.",
        "....",
    ],
    "K": [
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
        ".....",
    ],
    "L": [
        "#...",
        "#...",
        "#...",
        "#...",
        "#...",
        "#...",
        "####",
        "....",
    ],
    "M": [
        "#...#",
        "##.##",
        "#.#.#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".....",
    ],
    "N": [
        "##..#",
        "##..#",
        "#.#.#",
        "#.#.#",
        "#..##",
        "#..##",
        "#...#",
        ".....",
    ],
    "O": [
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
        ".....",
    ],
    "P": [
        "###.",
        "#..#",
        "#..#",
        "###.",
        "#...",
        "#...",
        "#...",
        "....",
    ],
    "Q": [
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        ".###.",
        "....#",
    ],
    "R": [
        "###.",
        "#..#",
        "#..#",
        "###.",
        "##..",
        "#.#.",
        "#..#",
        "....",
    ],
    "S": [
        ".##.",
        "#..#",
        "#...",
        ".##.",
        "...#",
        "#..#",
        ".##.",
        "....",
    ],
    "T": [
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ],
    "U": [
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        ".##.",
        "....",
    ],
    "V": [
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        ".#.#.",
        ".#.#.",
        "..#..",
        ".....",
    ],
    "W": [
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        ".#.#.",
        ".....",
    ],
    "X": [
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        "#...#",
        ".....",
    ],
    "Y": [
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ],
    "Z": [
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#####",
        ".....",
    ],
    " ": [
        "..",
        "..",
        "..",
        "..",
        "..",
        "..",
        "..",
        "..",
    ],
    ".": [
        ".",
        ".",
        ".",
        ".",
        ".",
        ".",
        "#",
        ".",
    ],
    ",": [
        ".",
        ".",
        ".",
        ".",
        ".",
        ".",
        "#",
        "#",
    ],
    "!": [
        "#",
        "#",
        "#",
        "#",
        "#",
        ".",
        "#",
        ".",
    ],
}

fallback = [
    ".....",
    ".....",
    "#####",
    "##.##",
    "#.#.#",
    "##.##",
    "#####",
    ".....",
]
