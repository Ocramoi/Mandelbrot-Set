#!/usr/bin/env python3

from mandelbrot import mandelbrot  # Max iter within bounds check
from PIL import Image, ImageDraw
from PARAMS import (MAX_ITER,
                    IMG_WIDTH, IMG_HEIGHT,
                    REAL_START, REAL_END,
                    IM_START, IM_END,
                    BW, STORE, IMG_PROGRAM)  # Params
from multiprocessing import Pool

# Creates new image and drawing
img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255))
drawing = ImageDraw.Draw(img)

# Creates palette as needed
palette = []
if not BW:
    for rg in range(0, 256, 5):
        palette.append((255 - rg, rg, 0))
    for gb in range(0, 256, 5):
        palette.append((0, 255 - gb, gb))

# Create pixel grid
pixels = []
for x in range(0, IMG_WIDTH):
    for y in range(0, IMG_HEIGHT):
        pixels.append([x, y])


def colorPixel(pixel: [int, int]):
    """
    Color each pixel acording to its max element within bounds on the set
    """

    # Generates according complex number
    c = complex(REAL_START + (pixel[0] / IMG_WIDTH) * (REAL_END - REAL_START),
                IM_START + (pixel[1] / IMG_HEIGHT) * (IM_END - IM_START))
    # Checks max bounded iteration
    i = mandelbrot(c)
    # Apply color
    if BW:
        tone = int(i/MAX_ITER * 255)
        color = (tone, tone, tone)
    else:
        color = palette[int(i/MAX_ITER * (len(palette) - 1))]
    return color


def main():
    # Creates pixel color array
    colors = []
    with Pool() as p:
        # Maps pixels to pixel coloring function asynchronously
        colors = p.map(colorPixel, pixels)
        # Awaits processes and waits for them to finish
        p.close()
        p.join()

    # Draws each pixel with given color
    for pixel in range(0, len(pixels)):
        drawing.point(pixels[pixel], colors[pixel])
    # Shows generated image
    if STORE:
        img.save("set.png", "PNG")
    else:
        img.show(command=IMG_PROGRAM)


if __name__ == "__main__":
    main()
