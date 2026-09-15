"""The static checker must leave valid month expressions to Biber."""
from pathlib import Path
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
            (copy / 'tests').mkdir(parents=True)
            for name in ('check_latex.py', 'regression-words.txt'):
                shutil.copy2(root / 'tests' / name, copy / 'tests' / name)
            bib = copy / 'months.bib'
            # Own the fixture: real example records may eventually have no months.
            for value in (None, '{5}', '{May}', 'may'):
                with self.subTest(value=value):
                    month = '' if value is None else f'  month = {value},\n'
                    bib.write_text(
                        '@misc{month_fixture,\n  year = {2026},\n' + month + '}\n',
                        encoding='utf-8',
                    )
                    result = subprocess.run([sys.executable, 'tests/check_latex.py'], cwd=copy, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
