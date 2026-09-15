"""Regression tests for failure visibility, missing artifacts and warning policy."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('build', Path(__file__).parents[1] / 'scripts/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class DiagnosticsTests(unittest.TestCase):
    def test_missing_outputs_fail(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(len(build.audit(Path(d), 'main')[0]), 3)

    def test_errors_and_layout_warnings_remain_distinct(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'main.pdf').write_bytes(b'fixture')
            (p/'main.log').write_text("main.tex:3: LaTeX Warning: Citation 'missing' undefined\nOverfull \\hbox\n")
            (p/'main.blg').write_text('INFO - done\n')
            errors, warnings = build.audit(p, 'main')
            self.assertEqual(len(errors), 1)
            self.assertEqual(len(warnings), 1)

    def test_failed_command_keeps_log_and_exit_status(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d)/'failure.log'
            code = build.run([sys.executable, '-c', 'print("intentional failure"); raise SystemExit(7)'], log, False)
            self.assertEqual(code, 7)
            self.assertIn('intentional failure', log.read_text())
            self.assertIn('Exit: 7', log.read_text())

if __name__ == '__main__':
    unittest.main()
