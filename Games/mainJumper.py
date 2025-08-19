import os

from Jumper import Jumper

import sys
import termios
import tty
import select

def read_key_non_blocking():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        dr, dw, de = select.select([sys.stdin], [], [], 0.1)  # timeout 0.1s
        if dr:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

print("Tape sur une touche pour commencer, ² pour quitter")

game = Jumper()

key = read_key_non_blocking()
while not key:
    key = read_key_non_blocking()

game.init()

while not game.game_over:
    key = None
    for i in range(2):
        tmp_key = read_key_non_blocking()
        if tmp_key == '²' or tmp_key == ' ':
            key = tmp_key
    os.system('clear')
    if key:
        if key == ' ':
            game.play(True)
        if key == '²':
            break
    else:
        game.play(False)
