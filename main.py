import machine
import neopixel
import time

# ─── CONFIG ───────────────────────────────────────
LEFT_PIN    = 13
RIGHT_PIN   = 14
MOSFET_PIN  = 15
TAIL_PIN    = 2
BRAKE_PIN   = 3
LTURN_PIN   = 4
RTURN_PIN   = 5

NUM_LEDS    = 50
CHASE_DELAY = 5

# Colors
RED_BRIGHT  = (255, 0, 0)
RED_DIM     = (127, 0, 0)
RED_CHASE   = (255, 0, 0)
OFF         = (0,   0, 0)

# ─── SETUP ────────────────────────────────────────
left   = neopixel.NeoPixel(machine.Pin(LEFT_PIN),  NUM_LEDS)
right  = neopixel.NeoPixel(machine.Pin(RIGHT_PIN), NUM_LEDS)
mosfet = machine.Pin(MOSFET_PIN, machine.Pin.OUT)

tail_in  = machine.Pin(TAIL_PIN,  machine.Pin.IN, machine.Pin.PULL_DOWN)
brake_in = machine.Pin(BRAKE_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
lturn_in = machine.Pin(LTURN_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
rturn_in = machine.Pin(RTURN_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# ─── HELPERS ──────────────────────────────────────
def fill_both(color):
    left.fill(color)
    right.fill(color)
    left.write()
    right.write()

def clear_strips():
    fill_both(OFF)

# ─── STARTUP ANIMATION ────────────────────────────
def startup_animation():
    mosfet.value(1)
    mid = NUM_LEDS // 2

    for repeat in range(3):
        clear_strips()
        time.sleep_ms(100)

        for i in range(mid):
            left[mid - 1 - i]  = RED_BRIGHT
            left[mid + i]      = RED_BRIGHT
            right[mid - 1 - i] = RED_BRIGHT
            right[mid + i]     = RED_BRIGHT
            left.write()
            right.write()
            time.sleep_ms(CHASE_DELAY * 5)

        time.sleep_ms(200)
        clear_strips()
        time.sleep_ms(150)

    steps = 20
    for step in range(steps):
        brightness = int(255 - ((255 - 127) * step / steps))
        fill_both((brightness, 0, 0))
        time.sleep_ms(20)

    if tail_in.value():
        fill_both(RED_DIM)
    else:
        clear_strips()
        mosfet.value(0)

# ─── TURN SIGNAL CHASE ────────────────────────────
def chase_left():
    mosfet.value(1)
    bg = RED_DIM if tail_in.value() else OFF

    left.fill(OFF)
    left.write()

    for i in range(NUM_LEDS - 1, -1, -1):
        left[i] = RED_CHASE
        left.write()
        time.sleep_ms(CHASE_DELAY)

    left.fill(OFF)
    left.write()

    timeout = 0
    while not lturn_in.value() and timeout < 50:
        time.sleep_ms(10)
        timeout += 1

    if not lturn_in.value():
        left.fill(bg)
        left.write()
        if bg == OFF:
            mosfet.value(0)

def chase_right():
    mosfet.value(1)
    bg = RED_DIM if tail_in.value() else OFF

    right.fill(OFF)
    right.write()

    for i in range(NUM_LEDS - 1, -1, -1):
        right[i] = RED_CHASE
        right.write()
        time.sleep_ms(CHASE_DELAY)

    right.fill(OFF)
    right.write()

    timeout = 0
    while not rturn_in.value() and timeout < 50:
        time.sleep_ms(10)
        timeout += 1

    if not rturn_in.value():
        right.fill(bg)
        right.write()
        if bg == OFF:
            mosfet.value(0)
def chase_hazard():
    mosfet.value(1)
    bg = RED_DIM if tail_in.value() else OFF
    mid = NUM_LEDS // 2

    clear_strips()

    for i in range(mid):
        left[mid - 1 - i]  = RED_CHASE
        left[mid + i]      = RED_CHASE
        right[mid - 1 - i] = RED_CHASE
        right[mid + i]     = RED_CHASE
        left.write()
        right.write()
        time.sleep_ms(CHASE_DELAY * 2)

    clear_strips()

    timeout = 0
    while not (lturn_in.value() and rturn_in.value()) and timeout < 50:
        time.sleep_ms(10)
        timeout += 1

    if not (lturn_in.value() and rturn_in.value()):
        fill_both(bg)
        if bg == OFF:
            mosfet.value(0)

# ─── RUN STARTUP ──────────────────────────────────
mosfet.value(1)
startup_animation()

# ─── MAIN LOOP ────────────────────────────────────
while True:
    tail  = tail_in.value()
    brake = brake_in.value()
    lturn = lturn_in.value()
    rturn = rturn_in.value()
    hazard = lturn and rturn

    if hazard:
        chase_hazard()

    elif lturn:
        chase_left()

    elif rturn:
        chase_right()

    elif brake:
        mosfet.value(1)
        fill_both(RED_BRIGHT)

    elif tail:
        mosfet.value(1)
        fill_both(RED_DIM)

    else:
        clear_strips()
        mosfet.value(0)

    time.sleep_ms(10)