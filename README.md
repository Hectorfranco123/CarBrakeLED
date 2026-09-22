# CarBrakeLED
Custom sequential LED brake/turn signal light bar I made for my 2022 Toyota Camry using Raspberry Pi Pico and MicroPython


---

## Features
- Sequential turn signal animation (left/right)
- Hazard light animation (center outward)
- Brake light mode (full brightness)
- DRL/tail light mode (half brightness)
- Startup sweep animation on boot
- All controlled via Raspberry Pi Pico and MicroPython

---

## Parts List

| Part | Details | Approx Cost |
|------|---------|-------------|
| Raspberry Pi Pico | RP2040 | ~$4 |
| BTF-LIGHTING WS2812B LED Strip | 2.7mm narrow PCB, 160 LEDs/m, 5V, 1m roll | ~$8-12 |
| Frosted clear acrylic strip | Cut to size | ~$5 |
| MP1584EN Buck Converter | 12V -> 5V | ~$2-3 |
| 10F 5.5V Supercapacitor | Power buffer | ~$2-3 |
| 4x PC817 Optocouplers | Signal isolation | ~$1-2 |
| 1x 1000µF 6.3V Capacitor | LED strip protection | ~$1-2 |
| 1kΩ Resistors | Optocoupler input side | ~$1 |
| 220Ω Resistors | Data line protection | ~$1 |
| Heat shrink tubing set | Wire protection | ~$3-4 |
| 3M VHB double sided tape | Mounting | ~$4-5 |

**Total Estimated Cost: $30-40**

---

## Wiring

> Coming soon — wiring diagram will be added in a future update.

### Quick Reference

#### From Tail Light Harness (5 wires)
- Tail wire -> Buck converter IN+ AND Optocoupler 1 Pin 1 (via 1kΩ)
- Brake wire -> Buck converter IN+ AND Optocoupler 2 Pin 1 (via 1kΩ)
- Left turn wire -> Optocoupler 3 Pin 1 (via 1kΩ)
- Right turn wire -> Optocoupler 4 Pin 1 (via 1kΩ)
- Ground wire -> Buck converter IN- AND all 4 Optocoupler Pin 2s tied together

#### Buck Converter
- IN+ -> Tail + Brake wires tied together
- IN- -> Harness Ground
- OUT+ -> 5V rail
- OUT- -> Ground rail
- Adjust to exactly 5V

#### Supercapacitor (10F 5.5V)
- \+ -> 5V rail
- \- -> Ground rail

#### 1000µF Capacitor
- \+ -> 5V rail
- \- -> Ground rail

#### Pico
- VSYS -> 5V rail
- GND -> Ground rail

#### Optocoupler 1 — Tail Light
- Pin 1 -> 1kΩ -> Tail wire
- Pin 2 -> Harness Ground
- Pin 3 -> Pico GPIO 2
- Pin 4 -> 5V rail

#### Optocoupler 2 — Brake Light
- Pin 1 -> 1kΩ -> Brake wire
- Pin 2 -> Harness Ground
- Pin 3 -> Pico GPIO 3
- Pin 4 -> 5V rail

#### Optocoupler 3 — Left Turn
- Pin 1 -> 1kΩ -> Left turn wire
- Pin 2 -> Harness Ground
- Pin 3 -> Pico GPIO 4
- Pin 4 -> 5V rail

#### Optocoupler 4 — Right Turn
- Pin 1 -> 1kΩ -> Right turn wire
- Pin 2 -> Harness Ground
- Pin 3 -> Pico GPIO 5
- Pin 4 -> 5V rail

#### Left LED Strip
- 5V -> 5V rail
- GND -> Ground rail
- DIN -> 220Ω resistor -> Pico GPIO 13

#### Right LED Strip
- 5V -> 5V rail
- GND -> Ground rail
- DIN -> 220Ω resistor -> Pico GPIO 14

---

## Tuning

| Variable | Default | Description |
|----------|---------|-------------|
| NUM_LEDS | 50 | Number of LEDs per strip |
| CHASE_DELAY | 5 | ms between each LED in chase animation |
| RED_DIM | (127, 0, 0) | Tail light brightness |
| RED_BRIGHT | (255, 0, 0) | Brake light brightness |

---

## Notes
- Never have USB and car power connected simultaneously
- Code is saved as main.py on the Pico for auto-boot
- Wiring diagram coming in future update

---
