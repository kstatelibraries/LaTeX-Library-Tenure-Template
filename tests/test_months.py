"""The static checker must leave valid month expressions to Biber."""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


class MonthTests(unittest.TestCase):
    def test_month_representations_are_not_rejected(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'repo'
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', 'build', '__pycache__'))
            bib = next(p for p in copy.glob('*.bib') if re.search(r'month\s*=\s*\{[^}]*\}', p.read_text()))
            original = bib.read_text()
            for value in ('{5}', '{May}', 'may'):
                with self.subTest(value=value):
                    bib.write_text(re.sub(r'month\s*=\s*\{[^}]*\}', 'month = '+value, original, count=1))
                    result = subprocess.run([sys.executable, 'tests/check_latex.py'], cwd=copy, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
