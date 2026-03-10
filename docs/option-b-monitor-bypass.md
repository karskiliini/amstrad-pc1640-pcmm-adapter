# Vaihtoehto B: Monitorin sisäisen invertterin ohitus

Avataan PC-MM ja ohitetaan sen sisäinen TC74HC04-invertteri. Tämän jälkeen adapteri tarvitsee vain sync-yhdistämisen.

## Toimintaperiaate

PC-MM:n sisällä oleva TC74HC04 invertoi kaikki signaalit, koska PC1512 lähettää ne käänteisesti. Kun invertteri ohitetaan, monitori hyväksyy normaalit (active-high) signaalit suoraan PC1640:sta.

## Monitorin muokkaus

> **VAROITUS:** CRT-monitorin sisällä on hengenvaarallisia jännitteitä (jopa tuhansia voltteja). Anna monitorin olla irti verkkovirrasta vähintään 24 tuntia ja pura CRT:n jännitys ennen työskentelyä.

### Vaiheet

1. Irrota monitori verkkovirrasta ja anna purkautua **vähintään 24h**
2. Avaa PC-MM:n kotelo (ruuvit takapaneelissa)
3. Paikanna **TC74HC04** (hex inverter) piirilevyltä — se on lähellä videoliittimen sisääntulopistettä
4. Tee yksi seuraavista:

**Vaihtoehto B1: IC:n korvaaminen langoituksella**
- Irrota TC74HC04 kannastaan (jos IC-kanta) tai irrojuota
- Juota ohuet langat jokaisen portin sisääntulosta suoraan ulostuloon:
  - Pin 1 → Pin 2
  - Pin 3 → Pin 4
  - Pin 5 → Pin 6
  - Pin 9 → Pin 8
  - Pin 11 → Pin 10
  - Pin 13 → Pin 12
- Jätä VCC (pin 14) ja GND (pin 7) kytkettyinä

**Vaihtoehto B2: Piggyback-IC** (palautettava)
- Juota 74HC04 **päälle** uusi IC jonka sisääntulopinnit on kytketty suoraan ulostulopinneihin
- Tämä kumoaa invertoinnin (kaksi peräkkäistä invertteriä = läpikulku)
- Helpompi peruuttaa: poista vain päällimmäinen IC

## Signaalireitti (muokattu monitori)

```
PC1640 (DE-9)           ADAPTERI-PCB                 PC-MM (8-pin DIN)
═════════════           ════════════                 ═════════════════

Pin 3 (R)  ──────────── suora ─────────────────→  Pin 8 (Red)
Pin 4 (G)  ──────────── suora ─────────────────→  Pin 5 (Green)
Pin 5 (B)  ──────────── suora ─────────────────→  Pin 6 (Blue)
Pin 6 (I)  ──────────── suora ─────────────────→  Pin 2 (Intensity)

Pin 8 (H-Sync) ──→┐
                   ├──→ 74HC86 [XOR] ──────────→  Pin 1 (C-Sync)
Pin 9 (V-Sync) ──→┘

Pin 1 (GND) ────────────── GND ────────────────→  Pin 3, Pin 7 (GND)
                                                   Pin 4 (Black) ← VCC kautta 10kΩ
```

## IC-kytkennät

### U1: 74HC86 (Quad XOR, DIP-14)

```
Gate 1: Pin 1 (H-Sync) + Pin 2 (V-Sync) → Pin 3 (C-Sync) → DIN pin 1
Gate 2–4: käyttämättömät, sisääntulot GND:hen

Pin 14: VCC (+5V)
Pin 7:  GND
```

## Komponenttilista (BOM)

| Ref | Komponentti                   | Arvo/Tyyppi  | Kpl | Hinta  |
|-----|-------------------------------|--------------|-----|--------|
| U1  | 74HC86 quad XOR               | DIP-14       | 1   | ~0,50€ |
| C1  | Keraaminen kondensaattori     | 100nF        | 1   | ~0,05€ |
| R1  | Vastus (Black pull-up)        | 10kΩ 1/4W    | 1   | ~0,05€ |
| J1  | DE-9 uros, PCB-mount          | right-angle  | 1   | ~1,50€ |
| J2  | 8-pin DIN naaras, PCB-mount   | panel mount  | 1   | ~2,00€ |
| J3  | USB Micro-B tai 2-pin header  | 5V virta     | 1   | ~0,50€ |
|     | **PCB 2-layer (5 kpl)**       | FR4          | 1   | ~5€    |
|     |                               |              |     | ~12–15€|

## PCB-layout suuntaviiva

```
┌──────────────────────────────────┐
│                                  │
│  [J1: DE-9]   [U1]   [J2: DIN]  │
│   uros        HC86   naaras     │
│              [C1][R1]            │
│                   [J3: +5V/GND]  │
│                                  │
└──────────────────────────────────┘
Koko: ~40 × 25 mm, 2-layer, through-hole
```

## Edut

- Yksinkertaisempi adapteri (vain 1 IC)
- Suorat signaaliyhteydet R/G/B/I — ei ylimääräistä viivettä
- Pienempi PCB

## Haitat

- **Vaatii monitorin avaamisen** — CRT-jännitteet ovat vaarallisia
- PC-MM on keräilykohde — muokkaus voi laskea arvoa
- Jos invertteri ohitetaan, monitori **ei toimi enää PC1512:n kanssa** (ellei käytetä piggyback-menetelmää)
- Piggyback-menetelmä mahdollistaa palautuksen, mutta on kömpelömpi

## Palautettavuus

| Menetelmä           | Palautettavuus |
|---------------------|----------------|
| IC:n irrotus + langat | Vaikea — vaatii uuden TC74HC04:n juottamisen |
| Piggyback-IC        | Helppo — poista päällimmäinen IC |
| IC-kanta + irrotus  | Helppo — aseta alkuperäinen IC takaisin kantaan |

**Suositus:** Jos monitorissa on IC-kanta, irrota alkuperäinen IC ja korvaa se langoitetulla kannalla. Jos IC on juotettu suoraan, käytä piggyback-menetelmää.
