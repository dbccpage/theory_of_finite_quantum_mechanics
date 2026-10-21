"""Replay unresolved/new diagnostic and preflight faults with separate inputs."""
from copy import deepcopy
import check_entrypoints as core
from check_majorana import SPECS

SELECT = {
    'src.majorana.majorana_modes': {'float', 'output term cap omitted', 'parity degree preflight omitted', 'product degree cap omitted'},
    'src.majorana.native_exact_input': {'exponent work cap omitted'},
}
definitions = {}
for module, names in SELECT.items():
    definitions[module] = deepcopy(SPECS[module])
    definitions[module]['mutants'] = [m for m in SPECS[module]['mutants'] if m[0] in names]
definitions['src.majorana.majorana_modes']['mutants'].append((
    'integer class callback introduced (unique function site)',
    'def _require_int(value: object, role: str) -> int:\n    if issubclass(type(value), float):',
    'def _require_int(value: object, role: str) -> int:\n    if isinstance(value, float):'))
for module in ['src.majorana.scalar', 'src.majorana.native_exact_input']:
    if module not in definitions:
        definitions[module] = deepcopy(SPECS[module])
        definitions[module]['mutants'] = []
    definitions[module]['mutants'].append(('scalar text cap omitted',
        'if len(value) > MAX_TEXT_CHARACTERS:', 'if False and len(value) > MAX_TEXT_CHARACTERS:'))


if __name__ == '__main__':
    core.main(definitions, 'code/python/tests/test_majorana_boundaries_followup.py', 'majorana-followup')
