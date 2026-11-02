"""Exercise the counter CLIs against complete Markdown bodies and malformed input."""
from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent
MANY = "threads_many_worlds.md"
MEMO = "where_to_contest_multiverse_realism.md"
POCKET = "marbles_to_everett.md"


def post(body, number=3, stated=None):
    count = len(body) if stated is None else stated
    return f"## Post {number} — example ({count} characters)\n\n{body}\n\n"


def quote_document(filename, body, stated=None, lazy=False):
    heading = ("# 5. A Threads-safe formulation" if filename == MEMO
               else "### Pocket version (fits one post)")
    count = len(body) if stated is None else stated
    quoted = "\n".join(("> " if i == 0 or not lazy else "") + line
                       for i, line in enumerate(body.split("\n")))
    return f"{heading}\n\n{quoted}\n>\n> ({count} characters, counted programmatically.)\n\n"


class PostCounterTests(unittest.TestCase):
    def run_counter(self, script, texts):
        out, err = io.StringIO(), io.StringIO()
        # Run the actual __main__ path without creating or modifying manuscript files.
        with patch.object(Path, "read_text", lambda path, **kwargs: texts[path.name]), \
                redirect_stdout(out), redirect_stderr(err):
            with self.assertRaises(SystemExit) as stopped:
                runpy.run_path(str(ROOT / script), run_name="__main__")
        return stopped.exception.code, out.getvalue(), err.getvalue()

    def many(self, text):
        return self.run_counter("count_many_worlds.py", {MANY: text})

    def quotes(self, filename=MEMO, body="Everett removes one rule", **kwargs):
        texts = {MEMO: quote_document(MEMO, "Everett removes one rule"),
                 POCKET: quote_document(POCKET, "Marbles through two holes")}
        texts[filename] = quote_document(filename, body, **kwargs)
        return self.run_counter("count_threads_safe.py", texts)

    def test_current_manuscripts_pass(self):
        texts = {name: (ROOT / name).read_text(encoding="utf-8")
                 for name in (MANY, MEMO, POCKET)}
        for script in ("count_many_worlds.py", "count_threads_safe.py"):
            with self.subTest(script=script):
                self.assertEqual(self.run_counter(script, texts)[0], 0)

    def test_numbered_post_counts_all_lines_and_paragraphs(self):
        code, output, _ = self.many(post("first\nsecond\n\nthird"))
        self.assertEqual(code, 0)
        self.assertIn("19 characters", output)

    def test_numbered_post_rejects_overlong_continuation(self):
        # The old parser sees only the first 491 characters and reports success.
        body = "x" * 491 + "\n" + "y" * 100
        self.assertNotEqual(self.many(post(body, stated=491))[0], 0)

    def test_numbered_post_limits_unicode_and_eof(self):
        for body, expected in [("é🌌" * 250, 0), ("x" * 501, 1)]:
            with self.subTest(length=len(body)):
                self.assertEqual(self.many(post(body).rstrip("\n"))[0], expected)

    def test_numbered_post_rejects_malformed_heading(self):
        for text in [post("text").replace("characters)", "chars)"),
                     post("text").replace("## Post", "### Post"),
                     post("text").replace("## Post", "  ## Post"),
                     post("text").replace("Post 3", "Post three")]:
            with self.subTest(text=text):
                self.assertNotEqual(self.many(text)[0], 0)
                self.assertNotEqual(self.many(text + post("valid", number=4))[0], 0)

    def test_numbered_post_requires_nonempty_unique_posts(self):
        for text in ["", "# Draft\n\nNo posts.\n", "## Sources behind each claim\n",
                     post(""), post("one") + post("two")]:
            with self.subTest(text=text):
                self.assertNotEqual(self.many(text)[0], 0)

    def test_numbered_post_checks_declared_count(self):
        self.assertNotEqual(self.many(post("text", stated=3))[0], 0)

    def test_sources_are_excluded_but_cannot_hide_later_posts(self):
        sources = "## Sources behind each claim\n\n" + "citation " * 200 + "\n"
        self.assertEqual(self.many(post("text") + sources)[0], 0)
        self.assertNotEqual(self.many(post("text") + sources + post("later", number=4))[0], 0)

    def test_quote_counts_explicit_and_lazy_continuations(self):
        body = "Everett removes one rule\nand another\n\nA new paragraph."
        for filename in (MEMO, POCKET):
            for lazy in (False, True):
                with self.subTest(filename=filename, lazy=lazy):
                    code, output, _ = self.quotes(filename, body, lazy=lazy)
                    self.assertEqual(code, 0)
                    self.assertIn(f"{filename}: {len(body)} chars", output)

    def test_quote_rejects_overlong_continuation(self):
        for filename, start in [(MEMO, "Everett removes one rule"),
                                (POCKET, "Marbles through two holes")]:
            for lazy in (False, True):
                body = start.ljust(491, "x") + "\n" + "y" * 100
                with self.subTest(filename=filename, lazy=lazy):
                    self.assertNotEqual(self.quotes(filename, body, stated=491, lazy=lazy)[0], 0)

    def test_quote_limit_and_declared_count(self):
        self.assertEqual(self.quotes(body="x" * 500)[0], 0)
        self.assertNotEqual(self.quotes(body="x" * 501)[0], 0)
        self.assertNotEqual(self.quotes(body="text", stated=3)[0], 0)

    def test_quote_rejects_missing_duplicate_empty_or_malformed_sections(self):
        valid = quote_document(MEMO, "Everett removes one rule")
        for invalid in ["", valid + valid, quote_document(MEMO, ""),
                        valid.replace("characters,", "chars,"), valid + "> extra text\n"]:
            with self.subTest(invalid=invalid):
                texts = {MEMO: invalid, POCKET: quote_document(POCKET, "Marbles through two holes")}
                self.assertNotEqual(self.run_counter("count_threads_safe.py", texts)[0], 0)

    def test_quote_accepts_eof_and_ignores_next_section(self):
        texts = {MEMO: quote_document(MEMO, "Everett removes one rule").rstrip("\n"),
                 POCKET: quote_document(POCKET, "Marbles through two holes")
                 + "## Classroom kit\n\n" + "instruction " * 200}
        self.assertEqual(self.run_counter("count_threads_safe.py", texts)[0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
