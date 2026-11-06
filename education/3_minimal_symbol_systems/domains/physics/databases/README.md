# Finite-example SQL schemas

AuthorityEffect: None.

The `.sql` files in this directory store declared finite examples and implement
specific arithmetic or relational queries. Removed physical certificate tables
must not be restored as evidence. `REAL` columns use floating-point arithmetic.
Caller-supplied flags and residuals remain untrusted inputs; a query selecting a
flag does not recompute the underlying property.

See the [domain claim ledger](../claim_ledger.md) for the supported scope.
