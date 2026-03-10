# Vaihtoehto A: Ulkoinen adapteri (suositeltu)

Ei vaadi monitorin muokkausta. Kaksi IC:tä hoitavat signaalin invertoinnin ja sync-yhdistämisen.

## Toimintaperiaate

1. **74HC86 (XOR)** yhdistää erilliset H-Sync + V-Sync → Composite Sync
2. **74HC04 (invertteri)** kääntää R, G, B, I ja C-Sync signaalien polariteetin active-low -muotoon, jota PC-MM odottaa

## Signaalireitti

```
PC1640 (DE-9)           ADAPTERI-PCB                 PC-MM (8-pin DIN)
═════════════           ════════════                 ═════════════════

Pin 3 (R)  ──────────→  74HC04 [inv1] ──────────→  Pin 8 (Red)
Pin 4 (G)  ──────────→  74HC04 [inv2] ──────────→  Pin 5 (Green)
Pin 5 (B)  ──────────→  74HC04 [inv3] ──────────→  Pin 6 (Blue)
Pin 6 (I)  ──────────→  74HC04 [inv4] ──────────→  Pin 2 (Intensity)

Pin 8 (H-Sync) ──→┐
                   ├──→ 74HC86 [XOR] ──→ 74HC04 [inv5] ──→ Pin 1 (C-Sync)
Pin 9 (V-Sync) ──→┘

Pin 1 (GND) ────────────── GND ────────────────→  Pin 3, Pin 7 (GND)
                                                   Pin 4 (Black) ← VCC kautta 10kΩ
```

## IC-kytkennät

### U1: 74HC04 (Hex Inverter, DIP-14)

```
        ┌──── U1: 74HC04 ────┐
  R in →│ 1  [INV1]  14 │← VCC (+5V)
 R out ←│ 2          13 │← käyttämätön (→ GND)
  G in →│ 3  [INV2]  12 │→ käyttämätön
 G out ←│ 4          11 │← C-Sync in (U2 pin 3:sta)
  B in →│ 5  [INV3]  10 │→ C-Sync inv out → DIN pin 1
 B out ←│ 6           9 │← I in
   GND →│ 7           8 │→ I inv out → DIN pin 2
        └────────────────┘

Gate 1: Pin 1 (R in)      → Pin 2  (R inv)      → DIN pin 8
Gate 2: Pin 3 (G in)      → Pin 4  (G inv)      → DIN pin 5
Gate 3: Pin 5 (B in)      → Pin 6  (B inv)      → DIN pin 6
Gate 4: Pin 9 (I in)      → Pin 8  (I inv)      → DIN pin 2
Gate 5: Pin 11 (C-Sync)   → Pin 10 (C-Sync inv) → DIN pin 1
Gate 6: Pin 13 → GND (käyttämätön)
```

### U2: 74HC86 (Quad XOR, DIP-14)

```
          ┌──── U2: 74HC86 ────┐
 H-Sync →│ 1  [XOR1]  14 │← VCC (+5V)
 V-Sync →│ 2          13 │← GND (käyttämätön)
C-Sync  ←│ 3          12 │← GND (käyttämätön)
    GND →│ 4  [XOR2]  11 │→ (käyttämätön)
    GND →│ 5          10 │← GND (käyttämätön)
        →│ 6           9 │← GND (käyttämätön)
    GND →│ 7           8 │→ (käyttämätön)
          └────────────────┘

Gate 1: Pin 1 (H-Sync) + Pin 2 (V-Sync) → Pin 3 (C-Sync) → U1 pin 11
Gate 2–4: käyttämättömät, sisääntulot GND:hen
```

## Komponenttilista (BOM)

| Ref | Komponentti                   | Arvo/Tyyppi  | Kpl | Footprint   | Hinta  |
|-----|-------------------------------|--------------|-----|-------------|--------|
| U1  | 74HC04 hex inverter           | DIP-14       | 1   | DIP-14      | ~0,50€ |
| U2  | 74HC86 quad XOR               | DIP-14       | 1   | DIP-14      | ~0,50€ |
| C1  | Keraaminen kondensaattori     | 100nF        | 1   | C_Disc_5mm  | ~0,05€ |
| C2  | Keraaminen kondensaattori     | 100nF        | 1   | C_Disc_5mm  | ~0,05€ |
| R1  | Vastus (Black pull-up)        | 10kΩ 1/4W    | 1   | Axial_7.6mm | ~0,05€ |
| J1  | DE-9 uros, PCB-mount          | right-angle  | 1   | DE-9_Male   | ~1,50€ |
| J2  | 8-pin DIN naaras, PCB-mount   | panel mount  | 1   | DIN-8       | ~2,00€ |
| J3  | USB Micro-B tai 2-pin header  | 5V virta     | 1   | —           | ~0,50€ |
|     | **PCB 2-layer (5 kpl)**       | FR4          | 1   | ~50×35mm    | ~5€    |
|     |                               |              |     | **Yhteensä**| ~15–20€|

## PCB-layout suuntaviiva

```
┌─────────────────────────────────────────┐
│                                         │
│  [J1: DE-9]    [U1]  [U2]    [J2: DIN] │
│   uros         HC04  HC86    naaras     │
│               [C1]  [C2]               │
│                [R1]                      │
│                        [J3: +5V/GND]    │
│                                         │
└─────────────────────────────────────────┘
Koko: ~50 × 35 mm, 2-layer, through-hole
```

## Virransyöttö

IC:t tarvitsevat +5V, yhteensä < 30 mA. Vaihtoehdot:

1. **USB Micro-B / USB-C PCB:llä** — mikä tahansa puhelinlaturi käy (suositeltu)
2. **2-pin header** + erillinen 5V-lähde
3. **Haaroitus 14-pin DIN -virtakaapelista** — siistimpi mutta vaatii lisäkaapelin

## PC1640 asetukset

DIP-kytkin emolevyllä:
- **SW8 = OFF** → CGA-tila (pin 2 maadoitettu)
- Tarkista muut kytkimet CGA-yhteensopivuudelle

## Edut

- Ei monitorin muokkausta — täysin palautettavissa
- Vain 2 halpaa IC:tä, yksinkertainen kytkentä
- Helppo rakentaa myös protolevylle (perfboard)
- Monitori toimii edelleen PC1512:n kanssa ilman adapteria

## Haitat

- Tarvitsee erillisen 5V-virransyötön
- Hieman isompi kuin vaihtoehto B

## Rakentaminen protolevylle (nopea versio)

Jos haluat testata ennen PCB-tilausta:

1. Kiinnitä 74HC04 ja 74HC86 protolevylle
2. Kytke VCC (+5V) ja GND molempiin IC:ihin
3. Lisää 100nF kondensaattorit VCC/GND-pinnien viereen
4. Juota signaalijohtimet DE-9-liittimestä IC:ille ja IC:iltä DIN-liittimeen
5. Käytä USB-kaapelia virransyöttöön (leikkaa vanha USB-kaapeli, käytä +5V ja GND)
