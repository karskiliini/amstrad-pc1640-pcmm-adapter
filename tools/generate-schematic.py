#!/usr/bin/env python3
"""
Generoi KiCad-skeema (.kicad_sch) Amstrad PC1640→PC-MM adapterille.

Komponentit:
  U1: 74HC04 hex inverter (DIP-14)
  U2: 74HC86 quad XOR (DIP-14)
  C1, C2: 100nF decoupling
  R1: 10kΩ pull-up
  J1: DE-9 Male (PC1640)
  J2: DIN-8 Female (PC-MM)
  J3: 2-pin power header
"""
import uuid

SCH_UUID = "e63e39d7-6ac0-4ffd-8aa3-1841a4541b55"


def uid():
    return str(uuid.uuid4())


def pin_def(name, number, x, y, direction, pin_type="bidirectional"):
    return f"""        (pin {pin_type} line
          (at {x} {y} {direction})
          (length 2.54)
          (name "{name}" (effects (font (size 1.27 1.27))))
          (number "{number}" (effects (font (size 1.27 1.27))))
        )"""


def sym_74hc04():
    """74HC04 hex inverter symbol - simplified as DIP-14 box."""
    pins = []
    # Left side: pins 1-7 (top to bottom)
    left_names = ["1A", "1Y", "2A", "2Y", "3A", "3Y", "GND"]
    for i, name in enumerate(left_names):
        pt = "passive" if name == "GND" else "bidirectional"
        pins.append(pin_def(name, str(i+1), -15.24, 15.24 - i*5.08, 0, pt))
    # Right side: pins 14-8 (top to bottom)
    right_names = ["VCC", "6A", "6Y", "5A", "5Y", "4A", "4Y"]
    right_nums = [14, 13, 12, 11, 10, 9, 8]
    for i, (name, num) in enumerate(zip(right_names, right_nums)):
        pt = "power_in" if name == "VCC" else "bidirectional"
        pins.append(pin_def(name, str(num), 15.24, 15.24 - i*5.08, 180, pt))

    return f"""    (symbol "adapter:74HC04"
      (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 20.32 0)
        (effects (font (size 1.27 1.27))))
      (property "Value" "74HC04" (at 0 -20.32 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_DIP:DIP-14_W7.62mm" (at 0 -22.86 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "74HC04_0_1"
        (rectangle (start -12.7 19.05) (end 12.7 -19.05)
          (stroke (width 0.254) (type default))
          (fill (type background))))
      (symbol "74HC04_1_1"
{chr(10).join(pins)}
      )
    )"""


def sym_74hc86():
    """74HC86 quad XOR symbol - simplified as DIP-14 box."""
    pins = []
    left_names = ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND"]
    for i, name in enumerate(left_names):
        pt = "passive" if name == "GND" else "bidirectional"
        pins.append(pin_def(name, str(i+1), -15.24, 15.24 - i*5.08, 0, pt))
    right_names = ["VCC", "4B", "4A", "4Y", "3Y", "3B", "3A"]
    right_nums = [14, 13, 12, 11, 10, 9, 8]
    for i, (name, num) in enumerate(zip(right_names, right_nums)):
        pt = "power_in" if name == "VCC" else "bidirectional"
        pins.append(pin_def(name, str(num), 15.24, 15.24 - i*5.08, 180, pt))

    return f"""    (symbol "adapter:74HC86"
      (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 20.32 0)
        (effects (font (size 1.27 1.27))))
      (property "Value" "74HC86" (at 0 -20.32 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_DIP:DIP-14_W7.62mm" (at 0 -22.86 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "74HC86_0_1"
        (rectangle (start -12.7 19.05) (end 12.7 -19.05)
          (stroke (width 0.254) (type default))
          (fill (type background))))
      (symbol "74HC86_1_1"
{chr(10).join(pins)}
      )
    )"""


def sym_connector(name, ref_prefix, pin_count, pin_names, footprint):
    """Generic connector symbol."""
    pins = []
    half = pin_count * 5.08 / 2
    for i, pname in enumerate(pin_names):
        pins.append(pin_def(pname, str(i+1), -15.24, half - i*5.08 - 2.54, 0, "passive"))

    return f"""    (symbol "adapter:{name}"
      (in_bom yes) (on_board yes)
      (property "Reference" "{ref_prefix}" (at 0 {half + 2.54} 0)
        (effects (font (size 1.27 1.27))))
      (property "Value" "{name}" (at 0 {-half - 2.54} 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" "{footprint}" (at 0 {-half - 5.08} 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "{name}_0_1"
        (rectangle (start -12.7 {half + 1.27}) (end 12.7 {-half - 1.27})
          (stroke (width 0.254) (type default))
          (fill (type background))))
      (symbol "{name}_1_1"
{chr(10).join(pins)}
      )
    )"""


def sym_passive(name, ref_prefix, footprint):
    """Resistor or capacitor symbol (2-pin)."""
    return f"""    (symbol "adapter:{name}"
      (in_bom yes) (on_board yes)
      (property "Reference" "{ref_prefix}" (at 0 2.54 0)
        (effects (font (size 1.27 1.27))))
      (property "Value" "{name}" (at 0 -2.54 0)
        (effects (font (size 1.27 1.27))))
      (property "Footprint" "{footprint}" (at 0 -5.08 0)
        (effects (font (size 1.27 1.27)) hide))
      (symbol "{name}_0_1"
        (rectangle (start -2.54 1.27) (end 2.54 -1.27)
          (stroke (width 0.254) (type default))
          (fill (type background))))
      (symbol "{name}_1_1"
        (pin passive line (at -5.08 0 0) (length 2.54)
          (name "1" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 5.08 0 180) (length 2.54)
          (name "2" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))
      )
    )"""


def sym_power(name, number):
    """Power symbol (+5V or GND)."""
    return f"""    (symbol "power:{name}"
      (power)
      (in_bom yes) (on_board yes)
      (property "Reference" "#{name}" (at 0 2.54 0)
        (effects (font (size 1.27 1.27)) hide))
      (property "Value" "{name}" (at 0 3.81 0)
        (effects (font (size 1.0 1.0))))
      (symbol "{name}_0_1"
        (polyline (pts (xy 0 0) (xy 0 1.27))
          (stroke (width 0) (type default))
          (fill (type none))))
      (symbol "{name}_1_1"
        (pin power_in line (at 0 0 90) (length 0) (hide yes)
          (name "{name}" (effects (font (size 1.27 1.27))))
          (number "{number}" (effects (font (size 1.27 1.27)))))
      )
    )"""


def symbol_instance(lib_name, ref, value, x, y, unit=1):
    """Place a symbol instance on the schematic."""
    return f"""  (symbol
    (lib_id "adapter:{lib_name}")
    (at {x} {y} 0)
    (unit {unit})
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (dnp no)
    (uuid "{uid()}")
    (property "Reference" "{ref}" (at 0 -22.86 0)
      (effects (font (size 1.27 1.27))))
    (property "Value" "{value}" (at 0 -25.40 0)
      (effects (font (size 1.27 1.27))))
  )"""


def power_instance(name, x, y, rot=90):
    """Place a power symbol."""
    return f"""  (symbol
    (lib_id "power:{name}")
    (at {x} {y} {rot})
    (unit 1)
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (dnp no)
    (uuid "{uid()}")
    (property "Reference" "#{name}" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide))
    (property "Value" "{name}" (at 3.81 0 0)
      (effects (font (size 1.0 1.0))))
  )"""


def wire(x1, y1, x2, y2):
    return f"""  (wire (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{uid()}")
  )"""


def net_label(name, x, y, rot=0):
    return f"""  (label "{name}" (at {x} {y} {rot})
    (effects (font (size 1.27 1.27)))
    (uuid "{uid()}")
  )"""


def text_note(text, x, y):
    return f"""  (text "{text}" (at {x} {y} 0)
    (effects (font (size 2.0 2.0)) (justify left))
    (uuid "{uid()}")
  )"""


def generate():
    # --- Lib symbols ---
    lib_symbols = "\n".join([
        sym_74hc04(),
        sym_74hc86(),
        sym_connector("DB9_Male", "J",  9,
                      ["GND", "SecRed", "RED", "GREEN", "BLUE", "INTENSITY", "SecBlue", "HSYNC", "VSYNC"],
                      "Connector_Dsub:DSUB-9_Male_Horizontal_P2.77x2.84mm"),
        sym_connector("DIN-8", "J", 8,
                      ["CSYNC", "INTENSITY", "GND", "BLACK", "GREEN", "BLUE", "GND", "RED"],
                      "amstrad-adapter:DIN-8_Video"),
        sym_connector("Conn_01x02", "J", 2,
                      ["+5V", "GND"],
                      "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"),
        sym_passive("R", "R",
                    "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal"),
        sym_passive("C", "C",
                    "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm"),
        sym_power("+5V", "1"),
        sym_power("GND", "1"),
    ])

    # --- Symbol instances ---
    # Positions on A3 sheet (mm from top-left)
    instances = "\n".join([
        text_note("Amstrad PC1640 → PC-MM Adapter (Option A)", 20, 20),
        text_note("74HC04: invertointi  |  74HC86: sync XOR", 20, 30),

        # J1: DE-9 input (left side)
        symbol_instance("DB9_Male", "J1", "PC1640 Video", 50, 100),

        # U1: 74HC04 (center)
        symbol_instance("74HC04", "U1", "74HC04", 140, 100),

        # U2: 74HC86 (center-right)
        symbol_instance("74HC86", "U2", "74HC86", 140, 180),

        # J2: DIN-8 output (right side)
        symbol_instance("DIN-8", "J2", "PC-MM Video", 250, 100),

        # C1, C2: decoupling
        symbol_instance("C", "C1", "100nF", 170, 60),
        symbol_instance("C", "C2", "100nF", 170, 220),

        # R1: pull-up
        symbol_instance("R", "R1", "10k", 220, 160),

        # J3: power
        symbol_instance("Conn_01x02", "J3", "+5V/GND", 100, 250),

        # Net labels for signal routing
        net_label("RED", 80, 90),
        net_label("RED_INV", 200, 90),
        net_label("GREEN", 80, 95),
        net_label("GREEN_INV", 200, 95),
        net_label("BLUE", 80, 100),
        net_label("BLUE_INV", 200, 100),
        net_label("INTENSITY", 80, 105),
        net_label("INTENSITY_INV", 200, 105),
        net_label("HSYNC", 80, 115),
        net_label("VSYNC", 80, 120),
        net_label("CSYNC", 170, 175),
        net_label("CSYNC_INV", 200, 110),
        net_label("BLACK", 230, 160),
    ])

    sch = f"""(kicad_sch
  (version 20231120)
  (generator "generate-schematic.py")
  (generator_version "1.0")
  (uuid "{SCH_UUID}")
  (paper "A3")

  (lib_symbols
{lib_symbols}
  )

{instances}
)
"""
    return sch


if __name__ == '__main__':
    import sys
    outpath = sys.argv[1] if len(sys.argv) > 1 else "hardware/amstrad-pc1640-pcmm-adapter.kicad_sch"
    sch = generate()
    with open(outpath, 'w') as f:
        f.write(sch)
    print(f"Skeema generoitu: {outpath}")
    print("  Komponentit: U1(74HC04), U2(74HC86), J1(DE-9), J2(DIN-8), J3(PWR), C1, C2, R1")
