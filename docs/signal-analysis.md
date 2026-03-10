# Signaalianalyysi: PC1640 ↔ PC-MM yhteensopivuus

## PC1640 videolähtö (DE-9 naaras, takapaneeli)

PC1640 käyttää standardia 9-pin DE-9 -videoliitintä. Signaalikartta riippuu käyttötilasta:

| Pin | CGA-tila         | EGA-tila          | MDA-tila          |
|-----|------------------|--------------------|-------------------|
| 1   | GND              | GND                | GND               |
| 2   | GND              | Sec. Red (r)       | GND               |
| 3   | Red (R)          | Primary Red (R)    | (ei käytössä)     |
| 4   | Green (G)        | Primary Green (G)  | (ei käytössä)     |
| 5   | Blue (B)         | Primary Blue (B)   | (ei käytössä)     |
| 6   | Intensity (I)    | Sec. Green (g)     | Intensity (I)     |
| 7   | (ei käytössä)    | Sec. Blue (b)      | Mono Video (V)    |
| 8   | **H-Sync** (+)   | **H-Sync** (+)     | **H-Sync** (+)    |
| 9   | **V-Sync** (+)   | **V-Sync** (-)     | **V-Sync** (-)    |

**Signaalitasot:** Kaikki digitaalisia TTL-tasoja (+5V HIGH / 0V LOW).

**DIP-kytkin SW8:** ON = EGA (pin 2 = Sec. Red), OFF = CGA/MDA (pin 2 = GND).

### Synkronointitaajuudet tilasta riippuen

| Tila     | H-Sync    | V-Sync   | H-polariteetti | V-polariteetti |
|----------|-----------|----------|----------------|----------------|
| CGA      | 15,7 kHz  | 60 Hz    | positiivinen   | positiivinen   |
| EGA      | 21,85 kHz | 60 Hz    | positiivinen   | negatiivinen   |
| MDA      | 18,43 kHz | 50 Hz    | positiivinen   | negatiivinen   |

---

## PC-MM monitorin sisääntulo (8-pin DIN)

PC-MM liittyy PC1512:een kahdella kaapelilla: video (8-pin DIN) ja virta (14-pin DIN).

### Video-liitin (8-pin DIN)

| Pin | Signaali                        | Johdon väri (tyypillinen) |
|-----|---------------------------------|---------------------------|
| 1   | **Composite Sync**              | valkoinen                 |
| 2   | Intensity                       | keltainen                 |
| 3   | GND                             | musta                     |
| 4   | "Black" (harmaasävykontrolli)   | harmaa                    |
| 5   | Green                           | vihreä                    |
| 6   | Blue                            | sininen                   |
| 7   | GND                             | musta                     |
| 8   | Red                             | punainen                  |

### Signaalin erikoispiirteet

- **Kaikki signaalit ovat invertoituja (active-low)**. PC1512 lähettää käänteiset TTL-signaalit.
- Monitorin sisällä on **TC74HC04 hex-invertteri** joka kääntää signaalit takaisin oikein.
- Harmaasävypainokertoimet monitorin sisällä: **R=2, G=4, B=1, I=8** → 16 harmaasävyä.
- Sisääntulossa 75Ω pull-down -vastukset ja 100Ω sarjavastukset.

### Toimintataajuudet

| Parametri      | Arvo      |
|----------------|-----------|
| H-taajuus      | 15,75 kHz |
| V-taajuus      | 60 Hz     |
| Näyttötila     | 200 juovaa progressiivinen |

---

## Virtaliitin (14-pin DIN, yhteinen molemmille)

PC-MM:n sisäinen virtalähde syöttää virran tietokoneelle tämän liittimen kautta. **Sama pinout molemmissa koneissa.**

| Pin | Signaali   |
|-----|------------|
| 1   | N/C        |
| 2   | GND        |
| 3   | +5V DC     |
| 4   | GND        |
| 5   | +5V DC     |
| 6   | N/C        |
| 7   | N/C        |
| 8   | GND        |
| 9   | -12V DC    |
| 10  | GND        |
| 11  | +12V DC    |
| 12  | GND        |
| 13  | -5V DC     |
| 14  | N/C        |

**Huom:** +5V on kahdella pinnillä (3, 5) virtankestävyyden vuoksi. Monitorin PSU: +5V max 7A, +12V max 4,9A.

---

## Yhteensopivuusongelmat

### 1. Taajuus — KRIITTINEN

PC-MM käsittelee **vain 15,75 kHz** horisontaalista taajuutta. PC1640:n EGA-tila tuottaa 21,85 kHz → **monitori ei synkronoidu**.

**Ratkaisu:** PC1640 asetetaan CGA-tilaan (SW8 = OFF), jolloin H-Sync = 15,7 kHz.

### 2. Signaalin polariteetti — KRIITTINEN

| Laite   | Signaalilogiikka |
|---------|------------------|
| PC1640  | Normaali (active-high TTL) |
| PC1512  | Invertoitu (active-low TTL) |
| PC-MM   | Odottaa invertoitua → sisäinen TC74HC04 kääntää takaisin |

Jos PC1640:n normaalit signaalit syötetään PC-MM:ään, sisäinen invertteri kääntää ne → **kuva on negatiivi**.

### 3. Synkronointi — KRIITTINEN

| Laite   | Sync-tyyppi |
|---------|-------------|
| PC1640  | Erilliset H-Sync (pin 8) + V-Sync (pin 9) |
| PC-MM   | Composite Sync (yhdistetty, pin 1) |

Tarvitaan XOR-piiri yhdistämään H-Sync + V-Sync → C-Sync.

### 4. Liitin — fyysinen ero

| Laite   | Liitin |
|---------|--------|
| PC1640  | DE-9 (9-pin D-sub) naaras |
| PC-MM   | 8-pin DIN uros (kaapelissa) |

### 5. Virta — YHTEENSOPIVA

14-pin DIN -virtaliitin on identtinen. PC-MM:n virtakaapeli kytkeytyy suoraan PC1640:een.

---

## Lähteet

- [Amstrad PC1640 Technical Reference Manual](https://www.seasip.info/AmstradXT/1640tech/section1.html)
- [Amstrad PC1512 Technical Reference Manual](https://www.seasip.info/AmstradXT/1512tech/section1.html)
- [PC1640 DIP Switch Settings](https://www.seasip.info/AmstradXT/pc1640dip.html)
- [Amstrad PC1640 Revival (RetroNerd)](https://retronerd.co.uk/amstrad-pc1640-revival/)
- [PC1512 Video Inverter Circuit (ctrl-alt-rees)](https://ctrl-alt-rees.com/2018-09-25-amstrad-pc1512-video-inverter-circuit.html)
- [Amstrad PC1640 Service Manual (PDF)](https://www.minuszerodegrees.net/manuals/Amstrad/Amstrad_PC1640_PC-MD_PC-CD_PC-ECD_Service_Manual_300dpi_Agujereado.pdf)
- [Amstrad PC1512 PC-MM Service Manual (Internet Archive)](https://archive.org/details/amstrad-pc1512-pc-mm-pc-cm-service-manual)
- [IBM MDA/CGA/EGA Pinouts](https://www.minuszerodegrees.net/mda_cga_ega/mda_cga_ega.htm)
