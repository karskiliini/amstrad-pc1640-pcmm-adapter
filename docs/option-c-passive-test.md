# Vaihtoehto C: Passiivinen adapteri ilman IC:tä (testaustarkoituksiin)

Nopea ja halpa testi ennen varsinaisen adapterin rakentamista. Ei vaadi IC-hankintoja.

## Toimintaperiaate

- R, G, B, I kytketään suoraan ilman inversiota
- H-Sync ja V-Sync yhdistetään vastusverkolla (epätarkempi kuin XOR, mutta voi riittää)
- **Kuva on negatiivi** (valkoinen teksti → musta, musta tausta → valkoinen) koska PC-MM:n sisäinen invertteri kääntää signaalit väärinpäin

## Kytkentä

```
PC1640 (DE-9)                                    PC-MM (8-pin DIN)
═════════════                                    ═════════════════

Pin 3 (R)  ─────────── suora ─────────────────→  Pin 8 (Red)
Pin 4 (G)  ─────────── suora ─────────────────→  Pin 5 (Green)
Pin 5 (B)  ─────────── suora ─────────────────→  Pin 6 (Blue)
Pin 6 (I)  ─────────── suora ─────────────────→  Pin 2 (Intensity)

Pin 8 (H-Sync) ──── 1kΩ ──→┐
                             ├──────────────→  Pin 1 (C-Sync)
Pin 9 (V-Sync) ──── 1kΩ ──→┘

Pin 1 (GND) ──────────── GND ────────────────→  Pin 3, Pin 7 (GND)
                                                 Pin 4 (Black) ← irti
```

## Tarvikkeet

| Komponentti              | Arvo    | Kpl | Hinta  |
|--------------------------|---------|-----|--------|
| Vastus                   | 1kΩ     | 2   | ~0,10€ |
| DE-9 uros (tai liitin)   | —       | 1   | ~1,50€ |
| 8-pin DIN naaras (tai kaapeli) | — | 1   | ~2,00€ |
| Protolevy / juotoslanka  | —       | 1   | ~1,00€ |
|                          |         |     | **~5€**|

## Mitä odottaa

### Kuva näkyy mutta on negatiivi
Tämä tarkoittaa, että signaalireitti toimii mutta inversio puuttuu. **Hyvä merkki** — siirry vaihtoehtoon A.

### Kuva rullaa pystysuunnassa
Composite sync ei toimi oikein vastusverkolla. Kokeile eri vastusarvoja (470Ω–2,2kΩ) tai siirry XOR-piiriin (vaihtoehto A/B).

### Ei kuvaa ollenkaan
Tarkista:
- Onko PC1640 CGA-tilassa (SW8 = OFF)?
- Ovatko GND-yhteydet kunnossa?
- Ovatko pinnit oikein (mittaa jännitteet)?

### Kuva on oikein päin
Epätodennäköistä, mutta jos näin käy, PC-MM:n sisäinen invertteri käyttäytyy eri tavalla kuin dokumentoitu. Hyvä uutinen — suora adapteri ilman invertteriä riittää.

## Rajoitukset

- **Ei tuotantokäyttöön** — vastusverkko-sync on epäluotettava
- Kuva on käänteinen — käytettävyys on heikko
- Vastusverkon impedanssi voi aiheuttaa häiriöitä kuvassa

## Tarkoitus

Tämä vaihtoehto on tarkoitettu **ainoastaan** ensimmäiseksi testiksi, jolla varmistetaan:
1. PC1640:n CGA-tilan taajuus on yhteensopiva PC-MM:n kanssa
2. Signaalireitti DE-9 → DIN toimii fyysisesti
3. Monitori syttyy ja näyttää jotain

Tulosten perusteella päätetään jatketaanko vaihtoehdolla A vai B.
