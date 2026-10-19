# Central finite-QM Python package

AuthorityEffect: None.

The application kernels now live here. `domain/` owns matrix and exact-number
carriers; `use_cases/` owns finite calculations and evidence rendering;
`entrypoints/` owns source intake, receipt replay, and the Block 03 command.
The existing application data and archived source packages retain their paths.

Application imports and seven former `quantum_physics` coordinates delegate to
the same central module objects. Importing the new package does not add flat
application directories to Python's search path. Legacy script facades temporarily
bootstrap the repository root and retain their command behavior.

`local_source_relocation.json` records the current CODA source blobs, former
imported overlaps, and each destination hash. The CPTP module retains both API
families. The correlation module retains CODA's corrected product-marginal
derivative. These are computational contracts and carry no theorem promotion.
