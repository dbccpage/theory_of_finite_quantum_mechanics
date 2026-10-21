"""Source-bound exact Clifford/Fock/scalar/codec and checker fault challenges."""
import sys
from pathlib import Path

import check_entrypoints as core

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'code/python'))
from src.majorana import test_majorana_control as old

TEST = 'code/python/tests/test_majorana_integrity.py'
SPECS = {
    'src.majorana.majorana_modes': {
        'source': 'code/python/src/majorana/majorana_modes.py',
        'old_tests': 'code/python/tests/test_majorana_modes.py',
        'mutants': [
            *[(name, ''.join(before), ''.join(after)) for name, before, after in old.LIBRARY_MUTANTS],
            ('class callback introduced', 'if issubclass(type(value), float):', 'if isinstance(value, float):'),
            ('overriding coefficient admitted', 'if type(value) is Fraction:', 'if isinstance(value, Fraction):'),
            ('mutable owned terms leaked', 'return dict(self._terms)', 'return self._terms'),
            ('reinitialization of monomial admitted', 'if hasattr(self, "modes"):', 'if False and hasattr(self, "modes"):'),
            ('word crossing parity inverted', 'crossings % 2 else 1', 'crossings % 2 == 0 else 1'),
            ('blade cancellation replaced by union', 'set(left).symmetric_difference(right)', 'set(left).union(right)'),
            ('monomial degree cap omitted', 'if len(modes) > MAX_MONOMIAL_MODES:', 'if False and len(modes) > MAX_MONOMIAL_MODES:'),
            ('product degree cap omitted', 'if len(merged) > MAX_MONOMIAL_MODES:', 'if False and len(merged) > MAX_MONOMIAL_MODES:'),
            ('input term cap omitted', 'if len(terms) > MAX_OPERATOR_TERMS:', 'if False and len(terms) > MAX_OPERATOR_TERMS:'),
            ('output term cap omitted', 'if monomial not in terms and len(terms) >= MAX_OPERATOR_TERMS:', 'if False and monomial not in terms and len(terms) >= MAX_OPERATOR_TERMS:'),
            ('pair work cap omitted', 'if a * b > MAX_TERM_PRODUCTS:', 'if False and a * b > MAX_TERM_PRODUCTS:'),
            ('degree work cap omitted', 'if work > MAX_TERM_MODE_WORK:', 'if False and work > MAX_TERM_MODE_WORK:'),
            ('fraction bits cap omitted', 'if max(value.numerator.bit_length(), value.denominator.bit_length()) > limit:', 'if False and max(value.numerator.bit_length(), value.denominator.bit_length()) > limit:'),
            ('parity degree preflight omitted', 'if sites > MAX_MONOMIAL_MODES // 2:', 'if False and sites > MAX_MONOMIAL_MODES // 2:'),
        ],
    },
    'src.majorana.majorana_fock_algebra': {
        'source': 'code/python/src/majorana/majorana_fock_algebra.py', 'old_tests': TEST,
        'mutants': [
            ('Gaussian product imaginary sign', 'self.re * other.im + self.im * other.re', 'self.re * other.im - self.im * other.re'),
            ('Gaussian reinitialization admitted', 'if hasattr(self, "re"):', 'if False and hasattr(self, "re"):'),
            ('Fock carrier reinitialization admitted', 'if hasattr(self, "_modes"):', 'if False and hasattr(self, "_modes"):'),
            ('occupation sign inverted', '-parity if bit else parity', 'parity if bit else -parity'),
            ('Jordan-Wigner prefix omitted', 'parity = -1 if (state >> (self._modes - mode)).bit_count() % 2 else 1', 'parity = 1'),
            ('lowering addition changed', 'odd[r][c] * half + even[r][c] * i_half', 'odd[r][c] * half - even[r][c] * i_half'),
            ('number uses empty bit', 'row == col and row & mask', 'row == col and not row & mask'),
            ('braid phase sign changed', 'phase = GaussianRat(Fraction(1, 2), Fraction(1, 2))', 'phase = GaussianRat(Fraction(1, 2), Fraction(0))'),
            ('parity mixing allowed', 'if (row.bit_count() - col.bit_count()) % 2 and not matrix[row][col].is_zero():', 'if False and (row.bit_count() - col.bit_count()) % 2 and not matrix[row][col].is_zero():'),
            ('nonsquare matrix admitted', 'if len(entries) != dimension:', 'if False and len(entries) != dimension:'),
            ('family different dimension admitted', 'if any(len(matrix) != dimension for matrix in matrices):', 'if False and any(len(matrix) != dimension for matrix in matrices):'),
            ('relation work cap omitted', 'if products > MAX_RELATION_PRODUCTS:', 'if False and products > MAX_RELATION_PRODUCTS:'),
            ('family cap omitted', 'if len(value) > limit:', 'if False and len(value) > limit:'),
            ('index upper end admitted', 'if not 1 <= index <= count:', 'if not 1 <= index <= count + 1:'),
            ('sector selector aliases admitted', 'if type(even) is not bool:', 'if False and type(even) is not bool:'),
        ],
    },
    'src.majorana.scalar': {
        'source': 'code/python/src/majorana/scalar.py', 'old_tests': TEST,
        'mutants': [
            ('class callback introduced', 'if issubclass(type(value), float):', 'if isinstance(value, float):'),
            ('Fraction subclass admitted', 'if type(value) is Fraction:', 'if isinstance(value, Fraction):'),
            ('scalar integer cap omitted', 'if value.bit_length() > MAX_SCALAR_BITS:', 'if False and value.bit_length() > MAX_SCALAR_BITS:'),
            ('quotient bit cap omitted', 'reduced = _bounded(numerator / denominator, "quotient")', 'reduced = numerator / denominator'),
            ('vector cap omitted', 'if len(values) > MAX_VECTOR_LENGTH:', 'if False and len(values) > MAX_VECTOR_LENGTH:'),
            ('canonical certificate bypassed', 'if text != canonical or q(text) != parsed:', 'if False and (text != canonical or q(text) != parsed):'),
            ('certificate reinitialized', 'if hasattr(self, "value"):', 'if False and hasattr(self, "value"):'),
            ('denominator sign erased', 'return f"{reduced.numerator}/{reduced.denominator}"', 'return f"{abs(reduced.numerator)}/{reduced.denominator}"'),
            ('decimal text accepted', 'if value == "" or "." in value or "e" in value or "E" in value:', 'if value == "":'),
        ],
    },
    'src.majorana.native_exact_input': {
        'source': 'code/python/src/majorana/native_exact_input.py', 'old_tests': TEST,
        'mutants': [
            ('native scalar aliases admitted', 'elif kind is Fraction:', 'elif isinstance(value, Fraction):'),
            ('integer bit cap omitted', 'if value.bit_length() > MAX_SCALAR_BITS:', 'if False and value.bit_length() > MAX_SCALAR_BITS:'),
            ('SymPy bits cap omitted', 'if max(numerator.bit_length(), denominator.bit_length()) > MAX_SCALAR_BITS:', 'if False and max(numerator.bit_length(), denominator.bit_length()) > MAX_SCALAR_BITS:'),
            ('exponent work cap omitted', 'if abs(exponent) > MAX_DECIMAL_EXPONENT:', 'if False and abs(exponent) > MAX_DECIMAL_EXPONENT:'),
            ('decimal quotient inverted', 'result /= _text_atom(parts[1])', 'result *= _text_atom(parts[1])'),
            ('vector cap omitted', 'if length > MAX_DIMENSION:', 'if False and length > MAX_DIMENSION:'),
            ('wire shape cap omitted', 'if max(rows, cols) > MAX_DIMENSION or rows * cols > MAX_MATRIX_ENTRIES:', 'if False and (max(rows, cols) > MAX_DIMENSION or rows * cols > MAX_MATRIX_ENTRIES):'),
            ('label cap omitted', 'if len(value) > MAX_LABEL_CHARACTERS:', 'if False and len(value) > MAX_LABEL_CHARACTERS:'),
            ('column restriction omitted', 'if cols != 1:', 'if False and cols != 1:'),
            ('zero row shape lost', '"cols": cols,', '"cols": 0,'),
        ],
    },
    'src.majorana.test_majorana_control': {
        'source': 'code/python/src/majorana/test_majorana_control.py',
        'old_tests': 'code/python/src/majorana/test_majorana_control.py',
        'mutants': [
            *[(name, ''.join(before), ''.join(after)) for name, before, after in old.HARNESS_MUTANTS],
            ('invalid source counted as killed', 'raise _fail("candidate could not be assessed; not counted as a kill", error=type(error).__name__) from error', 'return True'),
            ('prior module binding lost', 'sys.modules[name] = previous', 'sys.modules.pop(name, None)'),
            ('integer bit cap omitted', 'if value.bit_length() > MAX_INTEGER_BITS:', 'if False and value.bit_length() > MAX_INTEGER_BITS:'),
        ],
    },
}
DEPENDENCIES = [d['source'] for d in SPECS.values()] + ['code/python/src/majorana/__init__.py']
for spec in SPECS.values():
    spec['dependencies'] = DEPENDENCIES


if __name__ == '__main__':
    selected = {name: spec for name, spec in SPECS.items() if not sys.argv[1:] or name in sys.argv[1:]}
    if not selected:
        raise SystemExit('No declared Majorana subject selected')
    core.main(selected, TEST, 'majorana')
