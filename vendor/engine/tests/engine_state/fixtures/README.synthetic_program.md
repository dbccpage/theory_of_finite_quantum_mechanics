# Synthetic research-program test inputs

AuthorityEffect: None.

These inputs exercise parser, schema, and validator behavior only. They do not
replay a historical packet or establish research, publication, migration,
application-convergence, Lean, or independent-review outcomes.

The imported tests referenced five `docs/status/omega_conductor_*` packets that
are absent from AnomalonPy commit
`0a4e4c88bbb70c374cf61e20ac90558d745c18cf` and its reachable tracked history.
Their exact original bytes and Git object identities are unavailable.
`synthetic_program_fixture_custody.json` preserves the original test names and
unverified expected semantic hashes, and binds the tracked source files used
to construct the replacement unit inputs. Those expected hashes are not file
hashes or substitutes for the missing artifacts.

The claim-binding, foundations-registry, and application-convergence tests keep
their existing synthetic typed constructors and domain mutation tests. Their
unavailable historical-snapshot assertions are replaced by explicit JSON
parser refusal checks for unknown and missing fields. The migration and
published-series test constructors use the existing public schema constants
and declared coordinate table, with clearly synthetic hash-shaped values and
witness labels. Their original domain refusal checks remain active.

The replaced assertions of historical replay are withdrawn in this scope.
Historical replay remains `OPEN_UNAVAILABLE_SOURCE`. Production validators,
their pinned constants, and authority boundaries are unchanged. Successful
unit tests cannot fill this source gap.
