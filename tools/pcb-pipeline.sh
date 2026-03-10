#!/bin/bash
#
# PCB Pipeline: KiCad PCB → Freerouting → Gerbers → zip
#
# Käyttö:
#   ./tools/pcb-pipeline.sh hardware/amstrad-pc1640-pcmm-adapter
#
# Parametri on PCB-tiedoston polku ILMAN .kicad_pcb -päätettä.
#
set -euo pipefail

KICAD_PYTHON="/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3"
JAVA="/opt/homebrew/opt/openjdk/bin/java"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FREEROUTING="${SCRIPT_DIR}/freerouting.jar"

# --- Värit ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
fail()  { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }

# --- Parametrit ---
if [ $# -lt 1 ]; then
    echo "Käyttö: $0 <pcb-base-path>"
    echo "  Esim: $0 hardware/amstrad-pc1640-pcmm-adapter"
    exit 1
fi

BASE="$1"
PCB="${BASE}.kicad_pcb"
DSN="${BASE}.dsn"
SES="${BASE}.ses"
CAD="${BASE}.cad"
DIR="$(dirname "$BASE")"
NAME="$(basename "$BASE")"
GERBER_DIR="${DIR}/gerbers"
GERBER_ZIP="${DIR}/${NAME}-gerbers.zip"

[ -f "$PCB" ] || fail "PCB-tiedostoa ei löydy: $PCB"
[ -f "$KICAD_PYTHON" ] || fail "KiCad Pythonia ei löydy: $KICAD_PYTHON"

# --- 1. Validoi PCB ---
info "Validoidaan PCB..."
python3 "$SCRIPT_DIR/pcb-validate.py" "$PCB" || fail "Validointi epäonnistui"
ok "Validointi OK"

# --- 2. Export DSN ---
info "Exportoidaan DSN..."
$KICAD_PYTHON -c "
import pcbnew
board = pcbnew.LoadBoard('$PCB')
pcbnew.ExportSpecctraDSN(board, '$DSN')
" 2>/dev/null
[ -f "$DSN" ] || fail "DSN export epäonnistui"
ok "DSN: $DSN"

# --- 3. Freerouting ---
if [ -f "$FREEROUTING" ]; then
    info "Ajetaan Freerouting..."
    FREEROUTE_TIMEOUT="${FREEROUTE_TIMEOUT:-60}"
    $JAVA -jar "$FREEROUTING" -de "$DSN" -do "$SES" -mt 1 &
    FR_PID=$!
    for _i in $(seq 1 "$FREEROUTE_TIMEOUT"); do
        kill -0 $FR_PID 2>/dev/null || break
        sleep 1
    done
    if kill -0 $FR_PID 2>/dev/null; then
        warn "Freerouting timeout (${FREEROUTE_TIMEOUT}s) — pysäytetään"
        kill $FR_PID 2>/dev/null; sleep 2; kill -9 $FR_PID 2>/dev/null
    fi
    wait $FR_PID 2>/dev/null || true
    [ -f "$SES" ] || fail "Freerouting epäonnistui"
    ok "SES: $SES"

    # --- 4. Import SES + 5. Fill zones ---
    info "Importoidaan reitit ja täytetään zonet..."
    $KICAD_PYTHON -c "
import pcbnew
board = pcbnew.LoadBoard('$PCB')
pcbnew.ImportSpecctraSES(board, '$SES')
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
board.Save('$PCB')
print('OK: routes imported, zones filled')
" 2>/dev/null
    ok "Reitit ja zonet OK"
else
    warn "Freerouting.jar puuttuu — ohitetaan automaattireititys"
    warn "Lataa: https://github.com/freerouting/freerouting/releases"
fi

# --- 6. DRC ---
info "Ajetaan DRC-analyysi..."
MAX_UNCONNECTED="${MAX_UNCONNECTED:-0}"
python3 "$SCRIPT_DIR/pcb-drc-check.py" "$PCB" --max-unconnected "$MAX_UNCONNECTED"
DRC_EXIT=$?
if [ "$DRC_EXIT" -ne 0 ]; then
    fail "DRC hylätty — kriittisiä virheitä löytyi"
fi
ok "DRC hyväksytty"

# --- 7. Gerber + drill ---
info "Exportoidaan Gerberit..."
mkdir -p "$GERBER_DIR"
kicad-cli pcb export gerbers \
    --layers F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts \
    -o "$GERBER_DIR/" "$PCB"
kicad-cli pcb export drill -o "$GERBER_DIR/" "$PCB"
ok "Gerberit: $GERBER_DIR/"

# --- 8. GenCAD ---
info "Exportoidaan GenCAD..."
kicad-cli pcb export gencad -o "$CAD" "$PCB"
ok "GenCAD: $CAD"

# --- 9. Zip ---
info "Pakataan Gerber-zip..."
rm -f "$GERBER_ZIP"
(cd "$GERBER_DIR" && zip -q "../${NAME}-gerbers.zip" *)
ok "Zip: $GERBER_ZIP ($(du -h "$GERBER_ZIP" | cut -f1))"

# --- Yhteenveto ---
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} PCB Pipeline valmis!${NC}"
echo -e "${GREEN}========================================${NC}"
echo "  PCB:     $PCB"
echo "  Gerbers: $GERBER_ZIP"
echo "  GenCAD:  $CAD"
echo ""
echo "Lataa $GERBER_ZIP palveluun:"
echo "  https://jlcpcb.com"
echo "  https://www.pcbway.com"
