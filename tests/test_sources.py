"""Catch missing included files before starting TeX, including nested sources."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class SourceChecks(unittest.TestCase):
    def test_missing_nested_input_and_bibliography_fail(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'repo'
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', 'build', '__pycache__'))
            nested = copy / 'template' / 'layout.tex'
            original = nested.read_text()
            for command in (r'\input{missing-example}', r'\addbibresource{missing-example.bib}'):
                with self.subTest(command=command):
                    nested.write_text(original + '\n' + command + '\n')
                    result = subprocess.run([sys.executable, 'tests/check_latex.py'],
                                            cwd=copy, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn('template/layout.tex: missing', result.stderr)
                    self.assertIn('missing-example', result.stderr)

    def test_commented_input_is_not_required(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'repo'
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', 'build', '__pycache__'))
            nested = copy / 'template' / 'layout.tex'
            with nested.open('a') as output:
                output.write('\n% \\input{missing-example}\n')
            result = subprocess.run([sys.executable, 'tests/check_latex.py'],
                                    cwd=copy, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
