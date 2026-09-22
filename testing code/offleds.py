import machine
import neopixel
import time

PIN = 13
NUM_LEDS = 320


strip = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)


while True:
    # Turn everything off first
    for i in range(NUM_LEDS):
        strip[i] = (255, 0, 0)
    strip.write()

