# Vaihtoehto D: PC1640 EGA-tilassa

PC1640 pidetään EGA-tilassa (SW8 = ON). Tämä tuo kaksi erillistä haastetta riippuen ajettavasta ohjelmistosta.

## Taustaa: EGA-tilan kaksi toimintataajuutta

EGA-kortti (Paradise PEGA1A) vaihtaa automaattisesti kahden taajuuden välillä:

| Ohjelmatila          | Resoluutio | H-taajuus  | V-Sync polariteetti | PC-MM yhteensopiva? |
|----------------------|------------|------------|----------------------|---------------------|
| CGA-yhteensopiva     | 320×200 / 640×200 | **15,7 kHz** | positiivinen (+) | **Kyllä** |
| Natiivi EGA          | 640×350    | **21,85 kHz** | negatiivinen (-) | **Ei** |

**Suurin osa EGA-peleistä** käyttää 200-rivin tiloja (320×200, mode 0Dh/0Eh) jotka toimivat 15,7 kHz:llä. Vain osa ohjelmista vaatii 350-rivin tilaa.

---

## D1: EGA-tila, 200-rivin ohjelmat (15,7 kHz)

Toimii samalla adapterilla kuin vaihtoehto A, mutta tarvitsee **EGA 6-bit → CGA 4-bit RGBI** -signaalimappauksen.

### Ongelma: 6 signaalia → 4 signaalia

EGA-tilassa (SW8 = ON) PC1640 lähettää 6 digitaalista signaalia:

| Pin | Signaali | Rooli |
|-----|----------|-------|
| 2   | Sec. Red (r) | 1/3 punainen |
| 3   | Primary Red (R) | 2/3 punainen |
| 4   | Primary Green (G) | 2/3 vihreä |
| 5   | Primary Blue (B) | 2/3 sininen |
| 6   | Sec. Green (g) | 1/3 vihreä |
| 7   | Sec. Blue (b) | 1/3 sininen |

PC-MM odottaa 4 signaalia: **R, G, B, I** (Intensity).

### Ratkaisu: Intensity = OR(r, g, b)

CGA-yhteensopivissa ohjelmissa EGA-paletti mappaa värit niin, että intensiteetti näkyy sekundaarisignaaleissa. Yksinkertaisin konversio:

```
R = Pin 3 (Primary Red)
G = Pin 4 (Primary Green)
B = Pin 5 (Primary Blue)
I = OR(Pin 2, Pin 6, Pin 7)  ← yhdistetään kaikki sekundaarisignaalit
```

**Huomio:** Tämä mappaus ei ole täydellinen. CGA-väri 6 (ruskea, EGA-paletti 010100) tulkitaan väärin: sekundaari-vihreä=1 tuottaa Intensity=1, vaikka CGA:ssa ruskean intensiteetti on 0. **Monokroomonitorilla** tämä näkyy vain pienenä kirkkauserona yhdessä värissä — käytännössä merkityksetöntä.

### Signaalireitti

```
PC1640 (DE-9, EGA)      ADAPTERI-PCB                    PC-MM (8-pin DIN)
══════════════════      ════════════                    ═════════════════

Pin 3 (R)  ──────────→  74HC04 [inv] ──────────────→  Pin 8 (Red)
Pin 4 (G)  ──────────→  74HC04 [inv] ──────────────→  Pin 5 (Green)
Pin 5 (B)  ──────────→  74HC04 [inv] ──────────────→  Pin 6 (Blue)

Pin 2 (r)  ──→ D1 ──→┐
Pin 6 (g)  ──→ D2 ──→├──→ 74HC04 [inv] ───────────→  Pin 2 (Intensity)
Pin 7 (b)  ──→ D3 ──→┘
                (diode-OR)

Pin 8 (H-Sync) ──→┐
                   ├──→ 74HC86 [XOR] → 74HC04 [inv] → Pin 1 (C-Sync)
Pin 9 (V-Sync) ──→┘

Pin 1 (GND) ────────────── GND ───────────────────→  Pin 3, Pin 7 (GND)
                                                      Pin 4 (Black) ← VCC kautta 10kΩ
```

### Diode-OR toteutus

Kolme Schottky-diodia (esim. BAT85 tai 1N5817) yhdistävät sekundaarisignaalit:

```
Pin 2 (r) ──── ▷|──→┐
Pin 6 (g) ──── ▷|──→├──→ I (→ 74HC04 inverteriin)
Pin 7 (b) ──── ▷|──→┘
                     │
                    10kΩ → GND (pull-down)
```

Schottky-diodin jännitehäviö ~0,3V. TTL HIGH ≥ 2,4V → 2,4V - 0,3V = 2,1V → riittävä 74HC04:lle (kynnys ~1,5V).

### Komponenttilista (BOM)

| Ref | Komponentti                   | Arvo/Tyyppi    | Kpl | Hinta  |
|-----|-------------------------------|----------------|-----|--------|
| U1  | 74HC04 hex inverter           | DIP-14         | 1   | ~0,50€ |
| U2  | 74HC86 quad XOR               | DIP-14         | 1   | ~0,50€ |
| D1–D3 | Schottky-diodi             | BAT85 / 1N5817 | 3   | ~0,30€ |
| C1  | Keraaminen kondensaattori     | 100nF          | 1   | ~0,05€ |
| C2  | Keraaminen kondensaattori     | 100nF          | 1   | ~0,05€ |
| R1  | Vastus (Black pull-up)        | 10kΩ 1/4W      | 1   | ~0,05€ |
| R2  | Vastus (diode-OR pull-down)   | 10kΩ 1/4W      | 1   | ~0,05€ |
| J1  | DE-9 uros, PCB-mount          | right-angle    | 1   | ~1,50€ |
| J2  | 8-pin DIN naaras              | panel mount    | 1   | ~2,00€ |
| J3  | USB Micro-B / 2-pin header    | 5V virta       | 1   | ~0,50€ |
|     | **PCB 2-layer (5 kpl)**       | FR4            | 1   | ~5€    |
|     |                               |                |     | ~16–22€|

### Vaihtoehto: 74HC32 diodien sijaan

Jos haluat täysin digitaalisen ratkaisun, korvaa Schottky-diodit 74HC32:lla (quad OR gate):

```
Gate 1: Pin 2 (r) OR Pin 6 (g) → väliaikainen
Gate 2: väliaikainen OR Pin 7 (b) → Intensity
Gate 3–4: käyttämättömät (sisääntulot → GND)
```

Tämä lisää yhden IC:n mutta eliminoi diodien jännitehäviön.

---

## D2: Natiivi EGA 350-rivin tila (21,85 kHz) — vaatii scan-konvertterin

PC-MM **ei fyysisesti pysty** näyttämään 21,85 kHz signaalia. CRT:n vaakataajuuspiiri on suunniteltu vain 15,75 kHz:lle. Tarvitaan ulkoinen **scan rate -konvertteri** joka:

1. Vastaanottaa 21,85 kHz EGA-signaalin
2. Puskuroi kuvan muistiin (frame buffer)
3. Tulostaa sen uudelleen 15,75 kHz:llä

### Vaihtoehdot scan-konvertteriksi

#### OSSC Pro (~350€) — paras yksittäinen ratkaisu

```
PC1640 (DE-9 TTL) → vastusverkko (TTL→analog) → OSSC Pro → analog RGB 15kHz → adapteri → PC-MM
```

- Hyväksyy ~24 kHz tulotaajuuden (preset 350–400p lähteille)
- Voi tuottaa 240p / 15 kHz ulostuloa
- Tarvitsee TTL-to-analog konversion ennen OSSC:tä (yksinkertainen vastusverkko)
- Tarvitsee analog-to-TTL konversion OSSC:n jälkeen PC-MM:lle
- **Ongelmia:** kallein vaihtoehto, kaksi ylimääräistä konversiota, ei testattu spesifisesti EGA 21,85 kHz:llä

#### MCE2VGA + GBS-Control ketju (~50–90€) — budjettitasolla paras

```
PC1640 (DE-9 TTL) → MCE2VGA (EGA→VGA 31kHz) → GBS-Control (VGA→240p 15kHz) → adapteri → PC-MM
```

- **MCE2VGA** (~25–50€): FPGA-pohjainen, hyväksyy EGA TTL suoraan, tuottaa VGA-signaalin
- **GBS-8200 + GBS-Control** (~15–25€ + ESP8266 ~5€): vastaanottaa VGA:n, tuottaa 240p / 15 kHz
- Molemmat laitteet ovat hyvin testattuja erikseen
- **Ongelmia:** kaksi erillistä laitetta, lisäkaapelointi, mahdollinen viive (~1 frame)

#### Dual GBS-Control ketju (~50–80€) — epävarma

```
PC1640 → vastusverkko → GBS-Control #1 (21kHz→31kHz) → GBS-Control #2 (31kHz→15kHz) → adapteri → PC-MM
```

- Halvempi kuin MCE2VGA-ketju
- **Suuri riski:** GBS-8200 ei välttämättä lukitu 21,85 kHz taajuuteen (stock-firmware tukee 15/24/31 kHz)
- GBS-Control firmware laajentaa lukitusaluetta, mutta 21,85 kHz on "kuollut alue"
- **Ei suositella** ilman ennakkotestausta

### Hintavertailu scan-konvertterivaihtoehdoista

| Ratkaisu | Hinta | Luotettavuus | Laitteiden määrä |
|----------|-------|--------------|-------------------|
| OSSC Pro | ~350€ | Korkea (mutta ei testattu EGA:lla) | 1 + adapterit |
| MCE2VGA + GBS-Control | ~50–90€ | Hyvä (testatut komponentit) | 2 + adapteri |
| Dual GBS-Control | ~50–80€ | Epävarma (21 kHz lukitus?) | 2 + adapteri |
| Custom FPGA | ~25–50€ + työ | Riippuu toteutuksesta | 1 + adapteri |

---

## Ohjelmistoyhteensopivuus: tarvitsetko oikeasti 350-rivin tilaa?

Suurin osa DOS-peleistä käyttää **200-rivin tiloja** jotka toimivat 15,7 kHz:llä:

### 200-rivin EGA-pelejä (toimivat suoraan D1-adapterilla)

- King's Quest I–IV
- Space Quest I–III
- Leisure Suit Larry 1–2
- Maniac Mansion
- Lemmings
- Prince of Persia
- Commander Keen
- Wolfenstein 3D
- Doom (fallback)
- Monkey Island 1–2
- Suurin osa Sierra, LucasArts, Apogee -peleistä

### 350-rivin EGA-ohjelmia (vaativat scan-konvertterin)

- SimCity (1989)
- Microsoft Flight Simulator 3.0 / 5.0
- Windows 3.x EGA-tilassa
- Useimmat tuottavuusohjelmat (Word, Excel, Lotus 1-2-3)
- Osa strategiapeleistä (Gary Grigsby -sarjat)

**Jos käyttötarkoituksesi on pääasiassa DOS-pelejä, D1-ratkaisu (200-rivin tila) riittää todennäköisesti.**

---

## Suositus

| Käyttötarkoitus | Suositeltu ratkaisu | Hinta |
|-----------------|---------------------|-------|
| DOS-pelit (suurin osa) | **D1**: adapteri + diode-OR | ~16–22€ |
| 350-rivin ohjelmat (budjetti) | **D2**: MCE2VGA + GBS-Control | ~50–90€ + adapteri |
| 350-rivin ohjelmat (laatu) | **D2**: OSSC Pro | ~350€ + adapterit |
| Kaikki tilat ilman rajoituksia | Hanki EGA-monitori tai multisync | vaihtelee |
