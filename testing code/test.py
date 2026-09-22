import neopixel, machine
test = neopixel.NeoPixel(machine.Pin(13), 50)
test.fill((255, 0, 0))
test.write()