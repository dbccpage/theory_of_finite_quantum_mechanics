"""Regression checks for the collection verifier's evidence boundaries."""
import unittest

from verify import UniqueLoader, check_output, declared_symbols
import yaml


class VerifierBoundaryTests(unittest.TestCase):
    def test_python_reference_requires_top_level_declaration(self):
        source = '# def missing(): pass\ntext = "class Missing: pass"\ndef present():\n    pass\n'
        self.assertEqual(declared_symbols(source, '.py'), {'present'})

    def test_rust_comment_mentions_do_not_bind(self):
        source = '// pub fn missing() {}\n/*\npub struct Missing;\n/* nested */\n*/\npub fn present() {}\n'
        self.assertEqual(declared_symbols(source, '.rs'), {'present'})

    def test_lean_comment_mentions_do_not_bind(self):
        source = '-- theorem missing : True := by trivial\n/-\ntheorem Missing : True := by trivial\n/- nested -/\n-/\ntheorem present : True := by trivial\n'
        self.assertEqual(declared_symbols(source, '.lean'), {'present'})

    def test_duplicate_yaml_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            yaml.load('id: UQM-01\nid: UQM-02\n', Loader=UniqueLoader)

    def test_wrong_missing_extra_or_inexact_outputs_are_rejected(self):
        expected = {'p': '1/2'}
        for actual in ({'p': '1/3'}, {}, {'p': '1/2', 'extra': '0'}, {'p': 0.5}, {'p': '2/4'}):
            with self.subTest(actual=actual), self.assertRaises(ValueError):
                check_output('UQM-TEST', 'python', actual, expected)
        check_output('UQM-TEST', 'python', {'p': '1/2'}, expected)


if __name__ == '__main__':
    unittest.main()
