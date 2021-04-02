#!/usr/bin/env python3

from mandelbrot import mandelbrot
from PARAMS import MAX_ITER
import curses
import logging
from multiprocessing import Pool


logging.basicConfig(filename="out.log", level=logging.DEBUG)


class Vals:
    def __init__(self):
        self.STEP = 0.1
        self.MIN_L = -2
        self.MAX_T = 1
        self.SYMBS = [' ', '·', '-', '+', '#', '@', '░', '▒']


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


def getSymb(pixel: [int, int], objVals: Vals) -> chr:
    c = complex(objVals.MIN_L + pixel[0] * objVals.STEP,
                objVals.MAX_T - pixel[1] * objVals.STEP)
    i = mandelbrot(c)
    s = objVals.SYMBS[int(i/MAX_ITER * (len(objVals.SYMBS) - 1))]
    return s


def showSet(objVals: Vals, pixels: [],
            scr: "curses._CursesWindow"):
    scr.erase()
    height, width = scr.getmaxyx()
    symbMap = []
    concArray = list([pixel, objVals] for pixel in pixels)
    with Pool() as p:
        symbMap = p.starmap(getSymb, concArray)
    for s in symbMap:
        scr.addch(s)
    scr.refresh()


def createPixelGrid(scr: "curses._CursesWindow") -> [int]:
    pixels = []
    height, width = scr.getmaxyx()
    for h in range(0, height):
        for w in range(0, width):
            if h == height - 1 and w == width - 1:
                break
            pixels.append([w, h])
    return pixels


def main():
    scr = setupScr()
    objVals = Vals()

    pixels = createPixelGrid(scr)

    showSet(objVals=objVals, pixels=pixels, scr=scr)

    while True:
        inp = scr.getch()
        if inp == ord('q'):
            clenupExit(0)
        elif inp in [ord('h'), ord('a')]:
            objVals.MIN_L -= objVals.STEP
        elif inp in [ord('l'), ord('d')]:
            objVals.MIN_L += objVals.STEP
        elif inp in [ord('j'), ord('s')]:
            objVals.MAX_T -= objVals.STEP
        elif inp in [ord('k'), ord('w')]:
            objVals.MAX_T += objVals.STEP
        elif inp in [ord('+'), ord('K')]:
            objVals.STEP /= 1.1
        elif inp in [ord('-'), ord('J')]:
            objVals.STEP *= 1.1
        elif inp == ord('0'):
            objVals.STEP = 0.1
        elif inp == curses.KEY_RESIZE:
            pixels = createPixelGrid(scr)

        try:
            showSet(objVals=objVals, pixels=pixels, scr=scr)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
