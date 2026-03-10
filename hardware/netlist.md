# Netlist — Option A: External Adapter

Complete point-to-point wiring list for the adapter.

## Power

| From | To | Net |
|------|----|-----|
| J3 pin 1 | U1 pin 14, U2 pin 14, R1 (one end) | +5V |
| J3 pin 2 | U1 pin 7, U2 pin 7, J1 pin 1, J2 pin 3, J2 pin 7 | GND |
| C1 | U1 pin 14 → U1 pin 7 | Decoupling U1 |
| C2 | U2 pin 14 → U2 pin 7 | Decoupling U2 |

## Video signals (active-high → inverted via U1)

| PC1640 (J1) | Signal | U1 (74HC04) | PC-MM (J2) |
|-------------|--------|-------------|------------|
| J1 pin 3 | Red (R) | pin 1 → pin 2 (Gate 1) | J2 pin 8 |
| J1 pin 4 | Green (G) | pin 3 → pin 4 (Gate 2) | J2 pin 5 |
| J1 pin 5 | Blue (B) | pin 5 → pin 6 (Gate 3) | J2 pin 6 |
| J1 pin 6 | Intensity (I) | pin 9 → pin 8 (Gate 4) | J2 pin 2 |

## Sync (H+V → XOR → invert → C-Sync)

| PC1640 (J1) | Signal | U2 (74HC86) | U1 (74HC04) | PC-MM (J2) |
|-------------|--------|-------------|-------------|------------|
| J1 pin 8 | H-Sync | pin 1 (input A) | | |
| J1 pin 9 | V-Sync | pin 2 (input B) | | |
| | C-Sync (raw) | pin 3 (output) → | pin 11 (input) | |
| | C-Sync (inv) | | pin 10 (output) → | J2 pin 1 |

## Black signal

| From | Via | To | Net |
|------|-----|----|-----|
| +5V | R1 (10kΩ) | J2 pin 4 | Black pull-up |

## Unused pins

| IC | Pins | Connection |
|----|------|------------|
| U1 | pin 13 (Gate 6 input) | → GND |
| U2 | pin 4, 5 (Gate 2) | → GND |
| U2 | pin 9, 10 (Gate 3) | → GND |
| U2 | pin 12, 13 (Gate 4) | → GND |
| J1 | pin 2 (Sec. Red) | No connection (SW8=OFF grounds this) |
| J1 | pin 7 (Sec. Blue) | No connection |

## Wiring summary

```
                        +5V ─────────────────────────────────┐
                         │                                    │
                    ┌────┴────┐                          ┌────┴────┐
                    │ U1  14  │                          │ U2  14  │
                    │ 74HC04  │                          │ 74HC86  │
J1:3 (R) ─────────→│1      2│─────────→ J2:8 (Red)     │         │
J1:4 (G) ─────────→│3      4│─────────→ J2:5 (Green)   │         │
J1:5 (B) ─────────→│5      6│─────────→ J2:6 (Blue)    │         │
              GND ─→│7       │                     GND ─→│7       │
                    │       8│─────────→ J2:2 (Int)     │         │
J1:6 (I) ─────────→│9       │                          │         │
                    │      10│─────────→ J2:1 (C-Sync)  │         │
              ┌────→│11     │                          │         │
              │     │   12  │                          │         │
        GND ─→│    13│                          J1:8 ──→│1      3│──→ U1:11
              │     └────────┘                  J1:9 ──→│2       │
              │                                         │         │
              └─────────────────────────────────────────│3       │
                                                  GND ─→│4  5   │← GND
                                                  GND ─→│9  10  │← GND
                                                  GND ─→│12 13  │← GND
                                                        └────────┘

J2:4 (Black) ←── R1 (10kΩ) ←── +5V
J2:3, J2:7 ←── GND
J1:1 ←── GND

C1: U1 pin 14 ↔ U1 pin 7 (100nF, close to IC)
C2: U2 pin 14 ↔ U2 pin 7 (100nF, close to IC)
```
