"""Synthetic tests only: no real evaluation or voting records are used."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('confidentiality', Path(__file__).resolve().parents[1] / 'scripts/check_confidentiality.py')
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


class ConfidentialityTests(unittest.TestCase):
    def test_candidate_records_are_flagged(self):
        for text in ('Number voting yes: 12', 'Number voting no: & 3',
                     '12 Acceptable and 2 other votes',
                     'Supervisor comments: Synthetic review feedback.',
                     'Department head recommendation: Yes',
                     'Overall rating: Exceeds Expectations',
                     'The candidate was rated Meets Expectations.',
                     '[CONFIDENTIAL] example'):
            with self.subTest(text=text):
                self.assertTrue(SCAN.scan_blob('example.tex', text.encode()))

    def test_instructional_prose_and_public_examples_pass(self):
        for text in ('Previous tenure votes are removed from this example.',
                     'Supervisor comments: [redacted]',
                     'Describe service to the institution and profession.',
                     r'\Redacted{Evaluation}{The evaluation is omitted.}',
                     'Co-authored an article in Genetics in 2026.'):
            self.assertEqual([], SCAN.scan_blob('example.tex', text.encode()))

    def test_attachments_links_and_credentials_fail(self):
        private_url = 'https://' + 'example.' + 'sharepoint' + '.com/private'
        key = '-----BEGIN ' + 'PRIVATE KEY-----'
        for name, data in [('evidence.pdf', b'pretend PDF'), ('notes.md', b'\x00hidden'),
                           ('notes.md', private_url.encode()), ('key.txt', key.encode())]:
            with self.subTest(name=name):
                self.assertTrue(SCAN.scan_blob(name, data))
        self.assertTrue(SCAN.scan_blob('linked.tex', b'target', '120000'))

    def test_deleted_record_remains_detectable_in_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), '-c', 'user.name=Synthetic Test',
                    '-c', 'user.email=test@example.invalid', *args], stderr=subprocess.DEVNULL)
            git('init', '-b', 'main')
            record = root / 'example.tex'
            record.write_text('Supervisor comments: Synthetic private feedback.')
            git('add', '.'); git('commit', '-m', 'Synthetic fixture')
            record.write_text('Supervisor comments: [redacted]')
            git('add', '.'); git('commit', '-m', 'Redact fixture')
            self.assertEqual([], SCAN.check(root))
            results = SCAN.check(root, history=True)
            self.assertEqual(1, len(results))
            self.assertEqual('supervisor or committee record', results[0][2])
            self.assertNotIn('Synthetic private feedback', repr(results))

    def test_uncommitted_tracked_record_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-b', 'main', str(root)], check=True, capture_output=True)
            (root/'example.tex').write_text('Number voting yes: 12')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            self.assertTrue(SCAN.check(root))
