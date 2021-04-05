#!/usr/bin/env python3

from mandelbrot import mandelbrot
from PARAMS import MAX_ITER
import curses
import logging

# Visualizer symbols (chars)
SYMBS = [' ', '·', '-', '+', '#', '@', '░', '▒']
# Basic logging config
logging.basicConfig(filename="out.log", level=logging.DEBUG)


def clenupExit(exitCode: int) -> None:
    """ Destroys curses windows and exits with code [exitCode] """
    curses.endwin()
    exit(exitCode)


def setupScr() -> "curses._CursesWindow":
    """ Sets up curses screen """
    # Creates curses screen
    scr = curses.initscr()
    # Screen configs
    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    curses.curs_set(0)
    return scr


def showSet(left: float, top: float, step: float, scr: "curses._CursesWindow"):
    """
        Shows set with given left/top bound and "pixel" step
        on screen space
    """
    # Cleans screen
    scr.erase()
    # Get screen size
    height, width = scr.getmaxyx()
    # "Pixel" loop
    for h in range(0, height):
        for w in range(0, width):
            # Ignores last char (not supported by curses)
            if w == width - 1 and h == height - 1:
                break
            # Transforms "pixel" coordenates into complex number
            c = complex(left + w * step,
                        top - h * step)
            # Get max iteration on given "pixel"
            i = mandelbrot(c)
            # Shows correct char in gradient
            s = SYMBS[int(i/MAX_ITER * (len(SYMBS) - 1))]
            scr.addch(s)
    # Refresh screen
    scr.refresh()


def main():
    # Sets up new screen
    scr = setupScr()
    # Initial parameters
    minL = -2
    maxT = 1
    STEP = 0.1
    # Shows initial set
    showSet(left=minL, top=maxT, step=STEP, scr=scr)
    # Interactive loop
    while True:
        # Get input
        inp = scr.getch()
        # Exit option
        if inp == ord('q'):
            clenupExit(0)
        # Updates top/left boundries to move through the set
        elif inp in [ord('h'), ord('a')]:
            minL -= STEP
        elif inp in [ord('l'), ord('d')]:
            minL += STEP
        elif inp in [ord('j'), ord('s')]:
            maxT -= STEP
        elif inp in [ord('k'), ord('w')]:
            maxT += STEP
        # Updates step size, changing the "zoom"
        elif inp in [ord('+'), ord('K')]:
            STEP /= 1.1
        elif inp in [ord('-'), ord('J')]:
            STEP *= 1.1
        # Resets "zoom"
        elif inp in [ord('0'), ord('r'), ord('R')]:
            STEP = 0.1

        # Show updated set and log errors
        try:
            showSet(left=minL, top=maxT, step=STEP, scr=scr)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
