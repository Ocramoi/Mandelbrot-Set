#!/usr/bin/env python3

from mandelbrot import mandelbrot
from PARAMS import MAX_ITER
import curses
import logging


SYMBS = [' ', '·', '-', '+', '#', '@', '░', '▒']

logging.basicConfig(filename="out.log", level=logging.DEBUG)


def clenupExit(exitCode: int) -> None:
    """ Destroys curses windows and exits with code """
    curses.endwin()
    exit(exitCode)


def setupScr() -> "curses._CursesWindow":
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    curses.curs_set(0)
    return scr


def showSet(left: float, top: float, step: float, scr: "curses._CursesWindow"):
    scr.erase()
    height, width = scr.getmaxyx()
    for h in range(0, height):
        for w in range(0, width):
            if w == width - 1 and h == height - 1:
                break
            c = complex(left + w * step,
                        top - h * step)
            i = mandelbrot(c)
            s = SYMBS[int(i/MAX_ITER * (len(SYMBS) - 1))]
            scr.addch(s)
    scr.refresh()


def main():
    scr = setupScr()
    minL = -2
    maxT = 1
    STEP = 0.1
    showSet(left=minL, top=maxT, step=STEP, scr=scr)
    while True:
        inp = scr.getch()
        if inp == ord('q'):
            clenupExit(0)
        elif inp in [ord('h'), ord('a')]:
            minL -= STEP
        elif inp in [ord('l'), ord('d')]:
            minL += STEP
        elif inp in [ord('j'), ord('s')]:
            maxT -= STEP
        elif inp in [ord('k'), ord('w')]:
            maxT += STEP
        elif inp in [ord('+'), ord('K')]:
            STEP /= 1.1
        elif inp in [ord('-'), ord('J')]:
            STEP *= 1.1
        elif inp in [ord('0'), ord('r'), ord('R')]:
            STEP = 0.1

        try:
            showSet(left=minL, top=maxT, step=STEP, scr=scr)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
