# Amstrad PC1640 → PC-MM monitoriadapteri

## Löydösten yhteenveto

### PC1640 videolähtö (DE-9 naaras)

| Pin | CGA-tila         | EGA-tila          |
|-----|------------------|--------------------|
| 1   | GND              | GND                |
| 2   | GND              | Sec. Red (r)       |
| 3   | Red (R)          | Primary Red (R)    |
| 4   | Green (G)        | Primary Green (G)  |
| 5   | Blue (B)         | Primary Blue (B)   |
| 6   | Intensity (I)    | Sec. Green (g)     |
| 7   | (ei käytössä)    | Sec. Blue (b)      |
| 8   | **H-Sync** (+)   | **H-Sync** (+)     |
| 9   | **V-Sync** (+)   | **V-Sync** (-)     |

### PC-MM monitorin sisääntulo (8-pin DIN)

| Pin | Signaali                        |
|-----|---------------------------------|
| 1   | **Composite Sync**              |
| 2   | Intensity                       |
| 3   | GND                             |
| 4   | "Black" (harmaasävykontrolli)   |
| 5   | Green                           |
| 6   | Blue                            |
| 7   | GND                             |
| 8   | Red                             |

**Huom:** Kaikki signaalit ovat **invertoituja (active-low)** — PC-MM:n sisällä on TC74HC04-invertteri joka kääntää ne takaisin.

### Kriittiset yhteensopivuusongelmat

1. **Taajuus:** PC-MM toimii 15,75 kHz (CGA). PC1640 EGA-tilassa 21,85 kHz → **ei yhteensopiva**. Ratkaisu: PC1640 asetetaan **CGA-tilaan** (SW8 OFF).
2. **Signaalin polariteetti:** PC1640 lähettää normaalit (active-high) TTL-signaalit. PC-MM odottaa invertoituja (active-low). Monitorin sisäinen invertteri kääntäisi normaalit signaalit väärinpäin → **kuva on negatiivi**.
3. **Synkronointi:** PC1640 lähettää erilliset H-Sync + V-Sync. PC-MM vaatii **Composite Sync**.
4. **Liitin:** DE-9 vs 8-pin DIN.
5. **Virta:** 14-pin DIN -virtaliitin on **sama molemmissa** → suoraan yhteensopiva.

---

## Vaihtoehto A: Ulkoinen adapteri (suositeltu)

Ei vaadi monitorin muokkausta. Kaksi IC:tä hoitavat kaiken.

### Signaalireitti

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

### IC-kytkennät

**U1: 74HC04 (Hex Inverter)**

```
Pin 14: VCC (+5V)
Pin 7:  GND

Gate 1: Pin 1 (R in)      → Pin 2  (R inv)      → DIN pin 8
Gate 2: Pin 3 (G in)      → Pin 4  (G inv)      → DIN pin 5
Gate 3: Pin 5 (B in)      → Pin 6  (B inv)      → DIN pin 6
Gate 4: Pin 9 (I in)      → Pin 8  (I inv)      → DIN pin 2
Gate 5: Pin 11 (C-Sync)   → Pin 10 (C-Sync inv) → DIN pin 1
Gate 6: Pin 13 → GND (käyttämätön)
```

**U2: 74HC86 (Quad XOR)**

```
Pin 14: VCC (+5V)
Pin 7:  GND

Gate 1: Pin 1 (H-Sync) + Pin 2 (V-Sync) → Pin 3 (C-Sync) → U1 pin 11
Gate 2: Pin 4 → GND, Pin 5 → GND (käyttämätön)
Gate 3: Pin 9 → GND, Pin 10 → GND (käyttämätön)
Gate 4: Pin 12 → GND, Pin 13 → GND (käyttämätön)
```

### Komponenttilista

| #  | Komponentti                  | Arvo/Tyyppi | Kpl | Hinta (arvio) |
|----|------------------------------|-------------|-----|---------------|
| U1 | 74HC04 (DIP-14)             | Hex inverter | 1  | ~0,50€        |
| U2 | 74HC86 (DIP-14)             | Quad XOR     | 1  | ~0,50€        |
| C1 | Keraaminen kondensaattori   | 100nF        | 1  | ~0,05€        |
| C2 | Keraaminen kondensaattori   | 100nF        | 1  | ~0,05€        |
| R1 | Vastus (Black pull-up)      | 10kΩ         | 1  | ~0,05€        |
| J1 | DE-9 uros (PCB-mount)       | right-angle  | 1  | ~1,50€        |
| J2 | 8-pin DIN naaras (PCB-mount)| panel mount  | 1  | ~2,00€        |
| J3 | USB Micro-B tai 2-pin header| 5V virta     | 1  | ~0,50€        |
|    | **PCB (5 kpl)**             | 2-layer      | 1  | ~5€ + posti   |
|    |                              |             |     | **~15–20€**   |

### Edut

- Ei monitorin muokkausta
- Vain 2 IC:tä, yksinkertainen kytkentä
- Helppo rakentaa myös protolevylle
- Täysin palautettavissa (ei pysyviä muutoksia)

### Haitat

- Tarvitsee erillisen 5V-virransyötön (USB-laturi)
- Hieman isompi PCB kuin vaihtoehto B

---

## Vaihtoehto B: Monitorin sisäisen invertterin ohitus

Avataan PC-MM ja ohitetaan TC74HC04-invertteri. Tämän jälkeen adapteri tarvitsee vain sync-yhdistämisen.

### Monitorin muokkaus

1. Avaa PC-MM:n kotelo
2. Paikanna TC74HC04 (hex inverter) piirilevyltä
3. Juota ohuet langat jokaisen portin sisääntulosta suoraan ulostuloon (bypass)
4. TAI poista IC kannastaan ja korvaa se langoituksella

### Signaalireitti (muokattu monitori)

```
PC1640 (DE-9)           ADAPTERI-PCB                 PC-MM (8-pin DIN)
═════════════           ════════════                 ═════════════════

Pin 3 (R)  ──────────────────────────────────────→  Pin 8 (Red)
Pin 4 (G)  ──────────────────────────────────────→  Pin 5 (Green)
Pin 5 (B)  ──────────────────────────────────────→  Pin 6 (Blue)
Pin 6 (I)  ──────────────────────────────────────→  Pin 2 (Intensity)

Pin 8 (H-Sync) ──→┐
                   ├──→ 74HC86 [XOR] ──────────→  Pin 1 (C-Sync)
Pin 9 (V-Sync) ──→┘

Pin 1 (GND) ────────────── GND ────────────────→  Pin 3, Pin 7 (GND)
                                                   Pin 4 (Black) ← VCC kautta 10kΩ
```

### Komponenttilista

| #  | Komponentti                  | Arvo/Tyyppi | Kpl | Hinta (arvio) |
|----|------------------------------|-------------|-----|---------------|
| U1 | 74HC86 (DIP-14)             | Quad XOR     | 1  | ~0,50€        |
| C1 | Keraaminen kondensaattori   | 100nF        | 1  | ~0,05€        |
| R1 | Vastus (Black pull-up)      | 10kΩ         | 1  | ~0,05€        |
| J1 | DE-9 uros (PCB-mount)       | right-angle  | 1  | ~1,50€        |
| J2 | 8-pin DIN naaras (PCB-mount)| panel mount  | 1  | ~2,00€        |
| J3 | USB Micro-B tai 2-pin header| 5V virta     | 1  | ~0,50€        |
|    | **PCB (5 kpl)**             | 2-layer      | 1  | ~5€ + posti   |
|    |                              |             |     | **~12–15€**   |

### Edut

- Yksinkertaisempi adapteri (vain 1 IC)
- Suorat signaaliyhteydet R/G/B/I → ei viivettä

### Haitat

- **Vaatii monitorin avaamisen ja muokkauksen**
- PC-MM on keräilykohde — muokkaus voi laskea arvoa
- Jos invertteri ohitetaan väärin, monitori ei toimi PC1512:n kanssa enää
- CRT-monitorin sisällä on vaarallisia jännitteitä (huolellinen purkaus!)

---

## Vaihtoehto C: Passiivinen adapteri ilman IC:tä (testaustarkoituksiin)

Jos haluat kokeilla nopeasti ilman IC-hankintoja ja sinulla on protolevyä:

### Periaate

- Kytke R/G/B/I suoraan (ilman inversiota)
- Sync: yhdistä H-Sync ja V-Sync **vastusverkon** kautta (ei XOR, mutta voi toimia)
- Hyväksy että kuva on negatiivi (valkoinen teksti → musta teksti, musta tausta → valkoinen tausta)

### Kytkentä

```
PC1640 Pin 8 (H-Sync) ──── 1kΩ ──→┐
                                    ├──→ DIN Pin 1 (C-Sync)
PC1640 Pin 9 (V-Sync) ──── 1kΩ ──→┘
```

### Arvio

- **Toimii ehkä** — kuva on käänteinen mutta näet jotain
- Vastusverkon sync ei ole tarkka, kuva voi vääristyä reunoilta
- Hyvä **ensimmäiseksi testiksi** ennen PCB-suunnittelua

---

## Vertailutaulukko

| Ominaisuus                    | A: Ulkoinen adapteri | B: Monitorin muokkaus | C: Passiivinen testi |
|-------------------------------|----------------------|-----------------------|----------------------|
| IC:tä tarvitaan               | 2 (74HC04 + 74HC86) | 1 (74HC86)            | 0                    |
| Monitorin muokkaus            | Ei                   | Kyllä                 | Ei                   |
| Kuvan laatu                   | Oikea                | Oikea                 | Negatiivi/epätarkka  |
| Hinta                         | ~15–20€              | ~12–15€               | ~5€                  |
| Vaikeus                       | Helppo               | Keskitaso              | Erittäin helppo      |
| Palautettavuus                | Täysi                | Osittainen             | Täysi                |
| Sopii tuotantokäyttöön        | Kyllä                | Kyllä                 | Ei                   |

---

## PC1640 DIP-kytkinasetukset CGA-tilalle

PC1640:n emolevyllä:
- **SW8 = OFF** → CGA/MDA-tila (pin 2 maadoitettu)
- Muut kytkimet CGA-näyttötilaan sopiviksi

---

## Testaussuunnitelma

1. Mittaa adapterilta tulevat signaalit oskilloskoopilla/logiikka-analysaattorilla
2. Tarkista C-Sync: XOR(H-Sync, V-Sync) tuottaa oikean aaltomuodon
3. Tarkista inversio: signaalien polariteetti on käänteinen suhteessa sisääntuloon
4. Liitä PC-MM: jos kuva on negatiivi → inversio puuttuu/väärin. Jos rullaa → sync väärin
5. "Black"-pin (DIN pin 4): kokeile VCC / GND / irti — katso vaikutus kuvaan

---

## Avoimet kysymykset

- **"Black"-pinin (DIN pin 4) tarkka toiminta** — vaatii PC-MM:n huoltomanuaalin tarkemman tutkimisen
- **Sync-polariteetti** — XOR + inversio pitäisi tuottaa oikean tuloksen, mutta vaatii testauksen
- **PC1640 CGA-yhteensopivuus** — Paradise PEGA1A -piiri tukee CGA-tilaa, mutta ohjelmistoyhteensopivuus vaihtelee

---

## Lähteet

- [Amstrad PC1640 Technical Reference Manual (seasip.info)](https://www.seasip.info/AmstradXT/1640tech/section1.html)
- [Amstrad PC1512 Technical Reference Manual (seasip.info)](https://www.seasip.info/AmstradXT/1512tech/section1.html)
- [PC1640 DIP Switch Settings (seasip.info)](https://www.seasip.info/AmstradXT/pc1640dip.html)
- [Amstrad PC1640 Revival (RetroNerd)](https://retronerd.co.uk/amstrad-pc1640-revival/)
- [PC1512 Video Inverter Circuit (ctrl-alt-rees.com)](https://ctrl-alt-rees.com/2018-09-25-amstrad-pc1512-video-inverter-circuit.html)
- [PC1512 External PSU (ctrl-alt-rees.com)](https://ctrl-alt-rees.com/2018-09-10-amstrad-pc1512-building-an-external-power-supply.html)
- [Amstrad Video Liberator (GitHub)](https://github.com/reeshub/amstrad-pc1512-video-liberator)
- [Monotech EGA-Mono-Composite-Converter (GitHub)](https://github.com/monotech/EGA-Mono-Composite-Coverter)
- [Necroware MCE Adapter (GitHub)](https://github.com/necroware/mce-adapter)
- [GGLabs CGA2RGBv2](https://gglabs.us/node/2063)
- [Amstrad PC1640 Service Manual (PDF)](https://www.minuszerodegrees.net/manuals/Amstrad/Amstrad_PC1640_PC-MD_PC-CD_PC-ECD_Service_Manual_300dpi_Agujereado.pdf)
- [Amstrad PC1512 PC-MM Service Manual (Internet Archive)](https://archive.org/details/amstrad-pc1512-pc-mm-pc-cm-service-manual)
- [IBM MDA/CGA/EGA Pinouts (minuszerodegrees.net)](https://www.minuszerodegrees.net/mda_cga_ega/mda_cga_ega.htm)
