"""Opt-in real LaTeX failure test; run RUN_LATEX_INTEGRATION=1 with TeX installed.

Use a temporary copy so the deliberate error cannot alter portfolio sources.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(os.environ.get('RUN_LATEX_INTEGRATION') == '1', 'requires TeX; opt in with RUN_LATEX_INTEGRATION=1')
class LatexFailureTests(unittest.TestCase):
    def test_real_error_is_reported_and_retained(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'repo'
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', 'build', '__pycache__'))
            source = copy / 'main-cv.tex'
            source.write_text(source.read_text().replace('\\begin{document}', '\\begin{document}\n\\IntentionalBuildFailure', 1))
            result = subprocess.run([sys.executable, 'scripts/build.py', 'main-cv.tex'], cwd=copy,
                                    capture_output=True, text=True, timeout=180)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Undefined control sequence', result.stdout)
            self.assertIn('Stage: log audit for main-cv', result.stdout)
            self.assertNotIn('Stage: output ready', result.stdout)
            self.assertIn('Undefined control sequence', (copy/'build/main-cv.log').read_text())
            self.assertIn('Exit:', (copy/'build/main-cv-build.log').read_text())
            self.assertIn('Undefined control sequence', (copy/'build/main-cv-diagnostics.txt').read_text())
