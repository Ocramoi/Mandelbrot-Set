#!/usr/bin/env python3

from PARAMS import MAX_ITER, RADIUS


def __mandelbrot(z: complex, c: complex, n: int) -> int:
    """
        Recursively checks for iteration between radius,
        maxing out at defined iterations
    """
    if abs(z) > RADIUS or n >= MAX_ITER:
        return n

    return __mandelbrot(z**2 + c, c, n + 1)


def mandelbrot(c: complex) -> int:
    """
        Returns max iterations before set reaches bounds
    """
    return __mandelbrot(0, c, 0)
