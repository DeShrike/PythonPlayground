#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com) edited by foamyguy
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# set the variable equal to size of your neopixel strip
PIXELS = 30
# LED strip configuration:
LED_COUNT      = PIXELS   # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# All animations will take 256 total iteration steps to complete


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50, range_begin=0, range_end=-1, iteration_step=-1):
    """Wipe color across display a pixel at a time."""
    if range_end ==-1:
        range_end = strip.numPixels()

    # using modulous division and our range_begin offset to find which pixel
    # we need to change this step
    pixel_to_change = iteration_step % (range_end - range_begin) + range_begin

    # if it's the first pixel wipe the range clear
    if pixel_to_change - range_begin  == 0:
        for i in range(range_begin, range_end):
            strip.setPixelColor(i, Color(0,0,0))

    strip.setPixelColor(int(pixel_to_change), color)
    strip.show()
    if wait_ms > 0:
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, range_begin=0, range_end=-1, iteration_step=-1):
    """Movie theater light style chaser animation."""
    if range_end ==-1:
        range_end = strip.numPixels()

    # using modulous division to affect every 3rd pixel
    q = iteration_step % 3
    # loop over pixles and turn them on
    for i in range(range_begin, range_end, 3):
        # if the pixel is outside of our range then break out
        if i+q > range_end-1:
            break
        strip.setPixelColor(min(range_end-1,i+q), color)
    strip.show()
    time.sleep(wait_ms/1000.0)

    # loop over pixels and turn them off
    for i in range(range_begin, range_end, 3):
        # if the pixel is outside of our range then break out
        if i+q > range_end-1:
            break
        strip.setPixelColor(min(range_end-1,i+q), 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, range_begin=0, range_end=-1, iteration_step=-1):
    """Draw rainbow that fades across all pixels at once."""
    if range_end ==-1:
        range_end = strip.numPixels()

    # one color per iteration step
    j = iteration_step

    # loop over pixels in range and turn them on to current color from wheel
    for i in range(range_begin, range_end):
        strip.setPixelColor(i, wheel((i+j) & 255))
    strip.show()
    time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, range_begin=0, range_end=-1, iteration_step=-1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    if range_end ==-1:
        range_end = strip.numPixels()

    # one color per iteration step
    j = iteration_step

    # loop over pixels in range and turn them on to respective colors from wheel
    for i in range(range_begin, range_end):
        strip.setPixelColor(i, wheel((int(i * 256 / range_end-range_begin) + j) & 255))
    strip.show()
    time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50, range_begin=0, range_end=-1, iteration_step=-1):
    """Rainbow movie theater light style chaser animation."""
    if range_end ==-1:
        range_end = strip.numPixels()

    # one color per iteration step
    j = iteration_step

    # using modulous division to affect every 3rd pixel
    q = iteration_step % 3

    # loop over pixels and turn them on
    for i in range(range_begin, range_end, 3):
        # if the pixel is outside of our range then break out
        if i+q > range_end-1:
            break
        strip.setPixelColor(min(range_end-1,i+q), wheel((i+j) % 255))
    strip.show()
    time.sleep(wait_ms/1000.0)
    # loop over pixels and turn them off
    for i in range(range_begin, range_end, 3):
        # if the pixel is outside of our range then break out
        if i+q > range_end-1:
            break
        strip.setPixelColor(min(range_end-1,i+q), 0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            for i in range(256):

                #colorWipe(strip, Color(255, 0, 0), wait_ms=10, range_begin=0, range_end=PIXELS//3, iteration_step=i)  # Red wipe
                #colorWipe(strip, Color(0, 255, 0), wait_ms=10, range_begin=PIXELS//3, range_end=PIXELS//3*2, iteration_step=i)  # Blue wipe
                #colorWipe(strip, Color(0, 0, 255), wait_ms=10, range_begin=PIXELS//3*2, range_end=PIXELS, iteration_step=i)  # Green wipe
                rainbowCycle(strip, range_begin=0, range_end=PIXELS//3, iteration_step=i)
                #theaterChase(strip, Color(127, 127, 127), range_begin=PIXELS//3, range_end=PIXELS//3*2, iteration_step=i)
                theaterChaseRainbow(strip, range_begin=PIXELS//3, range_end=PIXELS//3*2, iteration_step=i)
                rainbow(strip, range_begin=PIXELS//3*2, range_end=PIXELS, iteration_step=i)

            # clear pixels
            for i in range(30):
                colorWipe(strip, Color(0,0,0), wait_ms=20, iteration_step=i)

    except KeyboardInterrupt:
        if args.clear:
            for i in range(30):
                colorWipe(strip, Color(0,0,0), wait_ms=10, iteration_step=i)
