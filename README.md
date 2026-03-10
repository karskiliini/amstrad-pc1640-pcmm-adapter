# amstrad-pc1640-pcmm-adapter

Video adapter for connecting an Amstrad PC1640 to an Amstrad PC-MM monochrome monitor.

The PC1640 and PC-MM were never designed to work together — the PC-MM was built for the PC1512. This project documents the signal incompatibilities and presents four adapter designs to bridge them.

## The Problem

| Issue | PC1640 output | PC-MM expects |
|-------|---------------|---------------|
| Connector | DE-9 (9-pin D-sub) | 8-pin DIN |
| Signal polarity | Normal (active-high TTL) | Inverted (active-low TTL) |
| Sync | Separate H-Sync + V-Sync | Composite Sync (combined) |
| Frequency | 21.85 kHz (EGA) / 15.7 kHz (CGA) | 15.75 kHz only |
| Power (14-pin DIN) | Same pinout | Same pinout — **compatible** |

**Solutions:** Run PC1640 in CGA mode (SW8 = OFF) for simplest adapter, or keep EGA mode (SW8 = ON) with additional signal conversion. See options below.

## Documentation

- **[Signal Analysis](docs/signal-analysis.md)** — Full pinouts, signal levels, frequency specs, and compatibility breakdown for both devices

## Adapter Options

### CGA mode (SW8 = OFF) — simpler adapter

| | Option A | Option B | Option C |
|---|---|---|---|
| **Approach** | External adapter | Monitor internal bypass | Passive test cable |
| **ICs needed** | 2 (74HC04 + 74HC86) | 1 (74HC86) | 0 |
| **Monitor mod** | No | Yes | No |
| **Image quality** | Correct | Correct | Inverted (negative) |
| **Cost** | ~15–20€ | ~12–15€ | ~5€ |
| **Difficulty** | Easy | Medium | Very easy |
| **Reversible** | Fully | Partially | Fully |
| **Recommended** | **Yes** | For advanced users | Testing only |

### [Option A: External Adapter](docs/option-a-external-adapter.md) (recommended for CGA mode)

Two ICs on a small PCB handle everything:
- **74HC04** inverts R, G, B, I, and C-Sync to match PC-MM's active-low input
- **74HC86** combines H-Sync + V-Sync into Composite Sync via XOR

No monitor modification needed. Fully reversible.

### [Option B: Monitor Internal Bypass](docs/option-b-monitor-bypass.md)

Bypass the PC-MM's internal TC74HC04 inverter, allowing standard TTL signals to pass through directly. The adapter only needs sync combining (one 74HC86). Smaller and simpler adapter PCB, but requires opening the CRT monitor.

### [Option C: Passive Test Cable](docs/option-c-passive-test.md)

Quick-and-dirty test with just two resistors and direct wiring. Image will be inverted (negative), but confirms that the signal path and frequency are compatible before committing to a PCB design.

---

### EGA mode (SW8 = ON) — preserves full EGA capability

### [Option D: EGA Mode Adapter](docs/option-d-ega-mode.md)

Keep the PC1640 in EGA mode for full 64-color palette capability. This option has two tiers:

**D1: 200-line programs (most DOS games)** — Same adapter as Option A, plus 3 Schottky diodes (or 74HC32 OR gate) to derive the Intensity signal from EGA's three secondary color lines. Works at 15.7 kHz. Cost: ~16–22€.

**D2: 350-line programs (Windows, productivity software)** — PC-MM cannot physically display 21.85 kHz. Requires an external scan rate converter:
- Budget: MCE2VGA + GBS-Control chain (~50–90€)
- Quality: OSSC Pro (~350€)

| | D1 (200-line) | D2 (350-line) |
|---|---|---|
| **Additional HW** | 3 diodes or 1 IC | Scan converter |
| **Programs** | Most DOS games | Windows, SimCity, Flight Sim |
| **H-frequency** | 15.7 kHz (native) | 21.85 kHz → 15.7 kHz (converted) |
| **Cost** | ~16–22€ | ~50–350€ + adapter |
| **Complexity** | Low | High |

## Chosen Design: Option A

Option A (external adapter, no monitor modification) is the selected approach.

### Hardware Files

- [`hardware/netlist.md`](hardware/netlist.md) — Complete point-to-point wiring with ASCII schematic
- [`hardware/bom.csv`](hardware/bom.csv) — Bill of materials with supplier part numbers
- [`hardware/amstrad-pc1640-pcmm-adapter.kicad_pro`](hardware/amstrad-pc1640-pcmm-adapter.kicad_pro) — KiCad project

## Project Status

- [x] Signal analysis and pinout research
- [x] Adapter design (schematic level)
- [x] Netlist and BOM
- [x] KiCad project skeleton
- [ ] KiCad schematic (.kicad_sch)
- [ ] PCB layout (.kicad_pcb)
- [ ] Prototype build and testing
- [ ] Gerber files for manufacturing

## References

- [Amstrad PC1640 Technical Reference Manual](https://www.seasip.info/AmstradXT/1640tech/section1.html)
- [Amstrad PC1512 Technical Reference Manual](https://www.seasip.info/AmstradXT/1512tech/section1.html)
- [PC1640 DIP Switch Settings](https://www.seasip.info/AmstradXT/pc1640dip.html)
- [PC1512 Video Inverter Circuit](https://ctrl-alt-rees.com/2018-09-25-amstrad-pc1512-video-inverter-circuit.html)
- [Amstrad Video Liberator (GitHub)](https://github.com/reeshub/amstrad-pc1512-video-liberator)
- [Necroware MCE Adapter (GitHub)](https://github.com/necroware/mce-adapter)
- [Monotech EGA-Mono-Composite-Converter (GitHub)](https://github.com/monotech/EGA-Mono-Composite-Coverter)

## License

This project is for personal use. Feel free to use and adapt for your own retro computing needs.
