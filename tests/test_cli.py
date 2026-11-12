import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CliTests(unittest.TestCase):
    def test_demo_matches_documented_output(self):
        result=subprocess.run([sys.executable,'main.py',*['samples/permissions.json']],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        expected=json.loads((ROOT/'samples'/'expected-output.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads(result.stdout),expected)

    def test_missing_input_is_handled(self):
        result=subprocess.run([sys.executable,'main.py','not-a-real-input-__demo__'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertNotIn('Traceback',result.stderr)
