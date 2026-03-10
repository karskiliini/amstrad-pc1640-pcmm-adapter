#!/usr/bin/env python3
"""
Generoi KiCad PCB-tiedosto Amstrad PC1640→PC-MM adapterille.

Komponentit:
  U1: 74HC04 (DIP-14) - hex inverter
  U2: 74HC86 (DIP-14) - quad XOR
  C1, C2: 100nF (disc 5mm, P2.50mm)
  R1: 10kΩ (axial, P7.62mm)
  J1: DE-9 Male (right-angle PCB mount)
  J2: DIN-8 Female (through-hole, custom footprint)
  J3: 2-pin header (power input)

Levy: 80 x 45 mm, 2-layer
"""
import uuid

# --- Board dimensions ---
BOARD_X = 100.0
BOARD_Y = 80.0
BOARD_W = 80.0
BOARD_H = 45.0

# --- Nets ---
NETS = [
    (0, ""),
    (1, "GND"),
    (2, "+5V"),
    (3, "RED"),
    (4, "RED_INV"),
    (5, "GREEN"),
    (6, "GREEN_INV"),
    (7, "BLUE"),
    (8, "BLUE_INV"),
    (9, "INTENSITY"),
    (10, "INTENSITY_INV"),
    (11, "HSYNC"),
    (12, "VSYNC"),
    (13, "CSYNC"),
    (14, "CSYNC_INV"),
    (15, "BLACK"),
]

# --- Component positions (absolute) ---
# Layout: J1(DE-9) left → U1,U2 side-by-side center → J2(DIN-8) right
# Board: 80 x 45 mm at (100,80)-(180,125)

# J1: DE-9 at left edge
J1_X, J1_Y = 108.0, 100.0

# U1: 74HC04 center-left (pin 1 top-left)
U1_X, U1_Y = 132.0, 88.0

# U2: 74HC86 center-right (side by side with U1)
U2_X, U2_Y = 145.0, 88.0

# C1: above U1 (decoupling)
C1_X, C1_Y = 133.0, 82.0

# C2: above U2 (decoupling)
C2_X, C2_Y = 146.0, 82.0

# R1: lower right area, near J2
R1_X, R1_Y = 157.0, 112.0

# J2: DIN-8 at right edge
J2_X, J2_Y = 170.0, 100.0

# J3: power header at bottom center
J3_X, J3_Y = 140.0, 121.0


def uid():
    return str(uuid.uuid4())


def make_pad(num, pad_type, shape, rel_x, rel_y, w, h, drill, net_id, net_name, layers="\"*.Cu\" \"*.Mask\""):
    drill_str = f"\n\t\t\t(drill {drill})" if drill else ""
    return f"""\t\t(pad "{num}" {pad_type} {shape}
\t\t\t(at {rel_x} {rel_y})
\t\t\t(size {w} {h}){drill_str}
\t\t\t(layers {layers})
\t\t\t(remove_unused_layers no)
\t\t\t(net {net_id} "{net_name}")
\t\t\t(uuid "{uid()}")
\t\t)"""


def make_footprint(fp_lib, ref, value, x, y, rot, pads_str):
    return f"""\t(footprint "{fp_lib}"
\t\t(layer "F.Cu")
\t\t(uuid "{uid()}")
\t\t(at {x} {y}{f' {rot}' if rot else ''})
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 -2 0)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uid()}")
\t\t\t(effects (font (size 1 1) (thickness 0.15)))
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at 0 -3.5 0)
\t\t\t(layer "F.Fab")
\t\t\t(uuid "{uid()}")
\t\t\t(effects (font (size 1 1) (thickness 0.15)))
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at 0 0 0) (layer "F.Fab") (hide yes)
\t\t\t(uuid "{uid()}")
\t\t\t(effects (font (size 1.27 1.27) (thickness 0.15)))
\t\t)
\t\t(property "Description" ""
\t\t\t(at 0 0 0) (layer "F.Fab") (hide yes)
\t\t\t(uuid "{uid()}")
\t\t\t(effects (font (size 1.27 1.27) (thickness 0.15)))
\t\t)
{pads_str}
\t\t(embedded_fonts no)
\t)"""


def dip14_pads(net_map):
    """Generate DIP-14 pads. net_map = {pin_num: (net_id, net_name)}"""
    pads = []
    for i in range(7):
        pin = i + 1
        nid, nname = net_map.get(pin, (0, ""))
        shape = "rect" if pin == 1 else "oval"
        pads.append(make_pad(pin, "thru_hole", shape, 0, i * 2.54, 1.6, 1.6, 0.8, nid, nname))
    for i in range(7):
        pin = 14 - i
        nid, nname = net_map.get(pin, (0, ""))
        pads.append(make_pad(pin, "thru_hole", "oval", 7.62, i * 2.54, 1.6, 1.6, 0.8, nid, nname))
    return "\n".join(pads)


def db9_male_pads(net_map):
    """Generate DE-9 Male horizontal pads."""
    pads = []
    # Row 1: pins 1-5, spacing 2.77mm
    for i in range(5):
        pin = i + 1
        nid, nname = net_map.get(pin, (0, ""))
        shape = "rect" if pin == 1 else "oval"
        pads.append(make_pad(pin, "thru_hole", shape, i * 2.77, 0, 1.6, 1.6, 1.0, nid, nname))
    # Row 2: pins 6-9, spacing 2.77mm, offset
    for i in range(4):
        pin = i + 6
        nid, nname = net_map.get(pin, (0, ""))
        pads.append(make_pad(pin, "thru_hole", "oval", 1.385 + i * 2.77, 2.84, 1.6, 1.6, 1.0, nid, nname))
    # Mounting holes
    pads.append(make_pad("MH1", "thru_hole", "oval", -5.08, 1.42, 3.0, 3.0, 2.2, 0, ""))
    pads.append(make_pad("MH2", "thru_hole", "oval", 16.16, 1.42, 3.0, 3.0, 2.2, 0, ""))
    return "\n".join(pads)


def din8_pads(net_map):
    """Generate 8-pin DIN female pads (full size, 262° pattern).

    Standard 8-pin DIN pin layout (looking at socket from front/mating side):
        6   1   5
      7           4
        8   3   2

    Approximate positions (mm from center), radius ~5.5mm:
    """
    import math
    positions = {
        1: (0, -5.5),       # top center
        2: (4.5, 3.0),      # bottom right
        3: (0, 3.0),        # bottom center
        4: (5.5, -1.5),     # right
        5: (3.5, -5.0),     # top right
        6: (-3.5, -5.0),    # top left
        7: (-5.5, -1.5),    # left
        8: (-4.5, 3.0),     # bottom left
    }
    pads = []
    for pin in range(1, 9):
        px, py = positions[pin]
        nid, nname = net_map.get(pin, (0, ""))
        shape = "rect" if pin == 1 else "oval"
        pads.append(make_pad(pin, "thru_hole", shape, px, py, 1.6, 1.6, 1.0, nid, nname))
    # Shield / mounting tabs
    pads.append(make_pad("SH1", "thru_hole", "oval", -7.5, 5.5, 3.0, 3.0, 2.2, 1, "GND"))
    pads.append(make_pad("SH2", "thru_hole", "oval", 7.5, 5.5, 3.0, 3.0, 2.2, 1, "GND"))
    return "\n".join(pads)


def cap_pads(net_p1, net_p2):
    """100nF disc capacitor, 2.5mm pitch."""
    pads = []
    pads.append(make_pad("1", "thru_hole", "rect", 0, 0, 1.6, 1.6, 0.8, net_p1[0], net_p1[1]))
    pads.append(make_pad("2", "thru_hole", "oval", 2.5, 0, 1.6, 1.6, 0.8, net_p2[0], net_p2[1]))
    return "\n".join(pads)


def resistor_pads(net_p1, net_p2):
    """Axial resistor, 7.62mm pitch."""
    pads = []
    pads.append(make_pad("1", "thru_hole", "rect", 0, 0, 1.6, 1.6, 0.8, net_p1[0], net_p1[1]))
    pads.append(make_pad("2", "thru_hole", "oval", 7.62, 0, 1.6, 1.6, 0.8, net_p2[0], net_p2[1]))
    return "\n".join(pads)


def header2_pads(net_p1, net_p2):
    """2-pin header, 2.54mm pitch."""
    pads = []
    pads.append(make_pad("1", "thru_hole", "rect", 0, 0, 1.7, 1.7, 1.0, net_p1[0], net_p1[1]))
    pads.append(make_pad("2", "thru_hole", "oval", 2.54, 0, 1.7, 1.7, 1.0, net_p2[0], net_p2[1]))
    return "\n".join(pads)


def generate():
    # Net definitions
    net_defs = "\n".join(f'\t(net {nid} "{nname}")' for nid, nname in NETS)

    # --- U1: 74HC04 ---
    # Pin mapping: 1=R_in, 2=R_inv, 3=G_in, 4=G_inv, 5=B_in, 6=B_inv,
    #              7=GND, 8=I_inv, 9=I_in, 10=CSYNC_inv, 11=CSYNC_in,
    #              12=unused, 13=GND(unused), 14=VCC
    u1_nets = {
        1: (3, "RED"), 2: (4, "RED_INV"),
        3: (5, "GREEN"), 4: (6, "GREEN_INV"),
        5: (7, "BLUE"), 6: (8, "BLUE_INV"),
        7: (1, "GND"),
        8: (10, "INTENSITY_INV"), 9: (9, "INTENSITY"),
        10: (14, "CSYNC_INV"), 11: (13, "CSYNC"),
        12: (0, ""), 13: (1, "GND"),
        14: (2, "+5V"),
    }
    u1 = make_footprint("Package_DIP:DIP-14_W7.62mm", "U1", "74HC04",
                        U1_X, U1_Y, 0, dip14_pads(u1_nets))

    # --- U2: 74HC86 ---
    # Pin mapping: 1=HSYNC, 2=VSYNC, 3=CSYNC, 4-6=GND(unused),
    #              7=GND, 8-13=GND(unused), 14=VCC
    u2_nets = {
        1: (11, "HSYNC"), 2: (12, "VSYNC"), 3: (13, "CSYNC"),
        4: (1, "GND"), 5: (1, "GND"), 6: (0, ""),
        7: (1, "GND"),
        8: (0, ""), 9: (1, "GND"), 10: (1, "GND"),
        11: (0, ""), 12: (1, "GND"), 13: (1, "GND"),
        14: (2, "+5V"),
    }
    u2 = make_footprint("Package_DIP:DIP-14_W7.62mm", "U2", "74HC86",
                        U2_X, U2_Y, 0, dip14_pads(u2_nets))

    # --- J1: DE-9 Male ---
    # Pin mapping: 1=GND, 2=nc, 3=RED, 4=GREEN, 5=BLUE,
    #              6=INTENSITY, 7=nc, 8=HSYNC, 9=VSYNC
    j1_nets = {
        1: (1, "GND"), 2: (0, ""), 3: (3, "RED"),
        4: (5, "GREEN"), 5: (7, "BLUE"), 6: (9, "INTENSITY"),
        7: (0, ""), 8: (11, "HSYNC"), 9: (12, "VSYNC"),
    }
    j1 = make_footprint("Connector_Dsub:DSUB-9_Male_Horizontal_P2.77x2.84mm",
                        "J1", "DB9_Male", J1_X, J1_Y, 0, db9_male_pads(j1_nets))

    # --- J2: DIN-8 Female ---
    # Pin mapping: 1=CSYNC_INV, 2=INTENSITY_INV, 3=GND, 4=BLACK,
    #              5=GREEN_INV, 6=BLUE_INV, 7=GND, 8=RED_INV
    j2_nets = {
        1: (14, "CSYNC_INV"), 2: (10, "INTENSITY_INV"),
        3: (1, "GND"), 4: (15, "BLACK"),
        5: (6, "GREEN_INV"), 6: (8, "BLUE_INV"),
        7: (1, "GND"), 8: (4, "RED_INV"),
    }
    j2 = make_footprint("amstrad-adapter:DIN-8_Video", "J2", "DIN-8",
                        J2_X, J2_Y, 0, din8_pads(j2_nets))

    # --- C1: 100nF near U1 ---
    c1 = make_footprint("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm",
                        "C1", "100nF", C1_X, C1_Y, 0,
                        cap_pads((2, "+5V"), (1, "GND")))

    # --- C2: 100nF near U2 ---
    c2 = make_footprint("Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm",
                        "C2", "100nF", C2_X, C2_Y, 0,
                        cap_pads((2, "+5V"), (1, "GND")))

    # --- R1: 10kΩ pull-up for BLACK ---
    r1 = make_footprint(
        "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal",
        "R1", "10k", R1_X, R1_Y, 0,
        resistor_pads((2, "+5V"), (15, "BLACK")))

    # --- J3: 2-pin power header ---
    j3 = make_footprint("Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
                        "J3", "+5V/GND", J3_X, J3_Y, 0,
                        header2_pads((2, "+5V"), (1, "GND")))

    # --- Board outline ---
    bx1, by1 = BOARD_X, BOARD_Y
    bx2, by2 = BOARD_X + BOARD_W, BOARD_Y + BOARD_H
    outline = f"""\t(gr_rect
\t\t(start {bx1} {by1})
\t\t(end {bx2} {by2})
\t\t(stroke (width 0.1) (type default))
\t\t(fill none)
\t\t(layer "Edge.Cuts")
\t\t(uuid "{uid()}")
\t)"""

    # --- Board label ---
    label = f"""\t(gr_text "PC1640→PC-MM Adapter v1.0"
\t\t(at {BOARD_X + BOARD_W/2} {BOARD_Y + 3} 0)
\t\t(layer "F.SilkS")
\t\t(uuid "{uid()}")
\t\t(effects (font (size 1.2 1.2) (thickness 0.15))
\t\t\t(justify left))
\t)"""

    # --- GND zone on B.Cu ---
    zone = f"""\t(zone
\t\t(net 1)
\t\t(net_name "GND")
\t\t(layer "B.Cu")
\t\t(uuid "{uid()}")
\t\t(hatch edge 0.5)
\t\t(connect_pads
\t\t\t(clearance 0.3)
\t\t)
\t\t(min_thickness 0.25)
\t\t(filled_areas_thickness no)
\t\t(fill yes
\t\t\t(thermal_gap 0.5)
\t\t\t(thermal_bridge_width 0.5)
\t\t)
\t\t(polygon
\t\t\t(pts
\t\t\t\t(xy {bx1} {by1})
\t\t\t\t(xy {bx2} {by1})
\t\t\t\t(xy {bx2} {by2})
\t\t\t\t(xy {bx1} {by2})
\t\t\t)
\t\t)
\t)"""

    # --- Assemble PCB ---
    pcb = f"""(kicad_pcb
\t(version 20241229)
\t(generator "generate-pcb.py")
\t(generator_version "1.0")
\t(general
\t\t(thickness 1.6)
\t\t(legacy_teardrops no)
\t)
\t(paper "A4")
\t(layers
\t\t(0 "F.Cu" signal)
\t\t(2 "B.Cu" signal)
\t\t(9 "F.Adhes" user "F.Adhesive")
\t\t(11 "B.Adhes" user "B.Adhesive")
\t\t(13 "F.Paste" user)
\t\t(15 "B.Paste" user)
\t\t(5 "F.SilkS" user "F.Silkscreen")
\t\t(7 "B.SilkS" user "B.Silkscreen")
\t\t(1 "F.Mask" user)
\t\t(3 "B.Mask" user)
\t\t(17 "Dwgs.User" user "User.Drawings")
\t\t(19 "Cmts.User" user "User.Comments")
\t\t(25 "Edge.Cuts" user)
\t\t(27 "Margin" user)
\t\t(31 "F.CrtYd" user "F.Courtyard")
\t\t(29 "B.CrtYd" user "B.Courtyard")
\t\t(35 "F.Fab" user)
\t\t(33 "B.Fab" user)
\t)
\t(setup
\t\t(pad_to_mask_clearance 0)
\t\t(allow_soldermask_bridges_in_footprints no)
\t\t(tenting front back)
\t\t(pcbplotparams
\t\t\t(layerselection 0x00000000_00000000_00010001_ffffffff)
\t\t\t(plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000)
\t\t\t(disableapertmacros no)
\t\t\t(usegerberextensions no)
\t\t\t(usegerberattributes yes)
\t\t\t(usegerberadvancedattributes yes)
\t\t\t(creategerberjobfile yes)
\t\t\t(dashed_line_dash_ratio 12.000000)
\t\t\t(dashed_line_gap_ratio 3.000000)
\t\t\t(svgprecision 4)
\t\t\t(plotframeref no)
\t\t\t(mode 1)
\t\t\t(useauxorigin no)
\t\t\t(hpglpennumber 1)
\t\t\t(hpglpenspeed 20)
\t\t\t(hpglpendiameter 15.000000)
\t\t\t(pdf_front_fp_property_popups yes)
\t\t\t(pdf_back_fp_property_popups yes)
\t\t\t(pdf_metadata yes)
\t\t\t(pdf_single_document no)
\t\t\t(dxfpolygonmode yes)
\t\t\t(dxfimperialunits yes)
\t\t\t(dxfusepcbnewfont yes)
\t\t\t(psnegative no)
\t\t\t(psa4output no)
\t\t\t(plot_black_and_white yes)
\t\t\t(sketchpadsonfab no)
\t\t\t(plotpadnumbers no)
\t\t\t(hidednponfab no)
\t\t\t(sketchdnponfab yes)
\t\t\t(crossoutdnponfab yes)
\t\t\t(subtractmaskfromsilk no)
\t\t\t(outputformat 1)
\t\t\t(mirror no)
\t\t\t(drillshape 1)
\t\t\t(scaleselection 1)
\t\t\t(outputdirectory "")
\t\t)
\t)
{net_defs}
{j1}
{u1}
{u2}
{c1}
{c2}
{r1}
{j2}
{j3}
{outline}
{label}
{zone}
)
"""
    return pcb


if __name__ == '__main__':
    import sys
    outpath = sys.argv[1] if len(sys.argv) > 1 else "hardware/amstrad-pc1640-pcmm-adapter.kicad_pcb"
    pcb = generate()
    with open(outpath, 'w') as f:
        f.write(pcb)
    print(f"PCB generoitu: {outpath}")
    print(f"  Levy: {BOARD_W} x {BOARD_H} mm")
    print(f"  Komponentit: J1(DE-9), U1(74HC04), U2(74HC86), C1, C2, R1, J2(DIN-8), J3(PWR)")
    print(f"  Netit: {len(NETS)}")
