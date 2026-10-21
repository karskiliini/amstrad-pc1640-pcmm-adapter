"""Exercise the actual shell/Python boundaries without KiCad or routing hardware."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


class PipelineFilenameBoundary(unittest.TestCase):
    def test_filenames_remain_data_in_both_python_calls(self):
        script = (Path(__file__).resolve().parents[1] / 'tools/pcb-pipeline.sh').read_text()
        calls = re.findall(r'(?:"\$KICAD_PYTHON"|\$KICAD_PYTHON) -c ".*?"[^\n]* 2>/dev/null', script, re.S)
        self.assertEqual(len(calls), 2)
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'pcbnew.py').write_text('''
import json, os
class Board:
    def Zones(self): return []
    def Save(self, path): record('save', path)
def record(kind, *args):
    with open(os.environ['CAPTURE'], 'a') as f: f.write(json.dumps([kind, *args]) + '\\n')
def LoadBoard(path): record('load', path); return Board()
def ExportSpecctraDSN(board, path): record('export', path)
def ImportSpecctraSES(board, path): record('import', path)
class ZONE_FILLER:
    def __init__(self, board): pass
    def Fill(self, zones): pass
''')
            for call in calls:
                for filename in ["board'); raise RuntimeError('filename executed'); #", "a board's \\name\nwith newline"]:
                    with self.subTest(call=call[:35], filename=filename):
                        capture = Path(tmp, 'calls.jsonl')
                        capture.unlink(missing_ok=True)
                        env = dict(os.environ, KICAD_PYTHON=sys.executable, PYTHONPATH=tmp,
                                   CAPTURE=str(capture), PCB=filename + '.kicad_pcb',
                                   DSN=filename + '.dsn', SES=filename + '.ses')
                        result = subprocess.run(['bash', '-c', call], env=env, capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        records = [json.loads(line) for line in capture.read_text().splitlines()]
                        self.assertEqual(records[0], ['load', env['PCB']])
                        if 'ExportSpecctraDSN' in call:
                            self.assertEqual(records[1], ['export', env['DSN']])
                        else:
                            self.assertEqual(records[1:], [['import', env['SES']], ['save', env['PCB']]])


if __name__ == '__main__':
    unittest.main()
