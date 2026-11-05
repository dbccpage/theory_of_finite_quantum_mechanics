"""Regression tests for self_audit_checks.py (Jeremy's review of 1eea606, finding 1).

Run:  python code/test_self_audit_checks.py
1. A reply of 501 characters must make the checker print FAIL and exit nonzero.
2. A missing replies file must make it exit nonzero (it used to print ALL PASS).
3. The submitted replies.md must pass with exit status 0.
4. A learning board that drops the second attempt time must fail S7a.
"""
import pathlib, subprocess, sys, tempfile, unittest

HERE = pathlib.Path(__file__).resolve().parent
CHECKER = HERE / "self_audit_checks.py"
REPLIES = HERE.parent / "01_thread" / "replies.md"
LEARNING = HERE.parent / "05_boards" / "learning_boards.html"


def run(replies_path):
    return subprocess.run([sys.executable, str(CHECKER), "--replies", str(replies_path)],
                          capture_output=True, text=True)


class CheckerExitStatus(unittest.TestCase):
    def test_submitted_replies_pass(self):
        r = run(REPLIES)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("ALL PASS", r.stdout)

    def test_501_char_reply_fails(self):
        text = REPLIES.read_text(encoding="utf-8")
        first = next(l for l in text.splitlines() if l.startswith("> "))
        long_text = text.replace(first, "> " + "x" * 501, 1)
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "replies.md"
            p.write_text(long_text, encoding="utf-8")
            r = run(p)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("FAIL S5.1", r.stdout)

    def test_missing_replies_fails(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(pathlib.Path(d) / "replies.md")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("FAIL S5 replies file present", r.stdout)
        self.assertNotIn("ALL PASS", r.stdout)


    def test_learning_board_without_attempt_time_fails(self):
        text = LEARNING.read_text(encoding="utf-8")
        self.assertIn("or 0.46 eV if every second", text)
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "learning_boards.html"
            p.write_text(text.replace("or 0.46 eV if every second", ""), encoding="utf-8")
            r = subprocess.run([sys.executable, str(CHECKER), "--replies", str(REPLIES), "--learning", str(p)],
                               capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("FAIL S7a", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
