"""Black-box regressions for ledger history and unavailable GitHub inventory."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'pending-drafts.sh'


class PendingDraftsTests(unittest.TestCase):
    def run_scan(self, fail=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / 'ledger.md'
            ledger.write_text('| `example.md` | `old-review` | old |\n'
                              '| `example.md` | `new-review` | latest |\n')
            gh = root / 'gh'
            gh.write_text('''#!/usr/bin/env python3
import os, sys
if os.environ.get('FAIL_INVENTORY') == '1':
    sys.exit(1)
endpoint = sys.argv[2]
if endpoint.endswith('/branches'):
    print('main head')
elif '/git/trees/' in endpoint:
    print('example.md new-blob')
elif endpoint.endswith('/contents/findings/example.md?ref=new-review'):
    print('new-blob')
else:
    sys.exit(1)
''')
            gh.chmod(0o700)
            return subprocess.run(['bash', str(SCRIPT)], text=True,
                                  capture_output=True,
                                  env=dict(os.environ, LEDGER=str(ledger),
                                           PATH=str(root)+os.pathsep+os.environ['PATH'],
                                           FAIL_INVENTORY='1' if fail else '0'))

    def test_latest_review_is_one_valid_ref(self):
        result = self.run_scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'pending: 0\n')

    def test_failed_inventory_is_unknown(self):
        result = self.run_scan(fail=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('queue unknown', result.stderr)
        self.assertNotIn('pending: 0', result.stdout)


if __name__ == '__main__':
    unittest.main()
