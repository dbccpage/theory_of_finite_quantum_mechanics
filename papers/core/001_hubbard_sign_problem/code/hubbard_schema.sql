-- Exact finite Meron and Hubbard relational evaluator. AuthorityEffect: None.
-- Rational values are reduced TEXT fractions; arithmetic uses qadd/qmul/qsum.
-- Native INTEGER operations act only on bounded counts, masks, and signs.
CREATE TABLE bit(bit INTEGER PRIMARY KEY CHECK(bit IN(0,1)));
INSERT INTO bit VALUES(0),(1);
CREATE TABLE experiment_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE hubbard_basis(state INTEGER PRIMARY KEY);
CREATE TABLE hubbard_hamiltonian(source INTEGER,target INTEGER,value TEXT,PRIMARY KEY(source,target));
CREATE INDEX hubbard_edge_source ON hubbard_hamiltonian(source);
CREATE TABLE scalar_matrix(side INTEGER,i INTEGER,j INTEGER,value TEXT,PRIMARY KEY(side,i,j));
CREATE TABLE dq_parameter(sites INTEGER,slices INTEGER,hs TEXT,fugacity TEXT,attractive INTEGER);
CREATE TABLE dq_site(site INTEGER PRIMARY KEY);
CREATE TABLE dq_field(mask INTEGER PRIMARY KEY);
CREATE TABLE dq_kinetic(i INTEGER,j INTEGER,value TEXT,PRIMARY KEY(i,j));
CREATE TABLE dq_product(mask INTEGER,spin INTEGER,i INTEGER,j INTEGER,value TEXT,PRIMARY KEY(mask,spin,i,j));
CREATE TABLE dq_next(mask INTEGER,spin INTEGER,i INTEGER,j INTEGER,value TEXT,PRIMARY KEY(mask,spin,i,j));
CREATE TABLE dq_determinant(mask INTEGER,spin INTEGER,value TEXT,log_fugacity_derivative TEXT,PRIMARY KEY(mask,spin));
CREATE VIEW dq_weight AS SELECT up.mask,up.value up,down.value down,
qmul(qmul(up.value,down.value),CASE WHEN attractive=1 THEN qpow(hs,sites*slices-2*popcount(up.mask)) ELSE '1' END) weight
FROM dq_determinant up JOIN dq_determinant down ON down.mask=up.mask AND down.spin=1 CROSS JOIN dq_parameter WHERE up.spin=0;

CREATE VIEW dq_number AS SELECT up.mask,
qdiv(qmul(qadd(qmul(up.log_fugacity_derivative,down.value),qmul(up.value,down.log_fugacity_derivative)),
 CASE WHEN attractive=1 THEN qpow(hs,sites*slices-2*popcount(up.mask)) ELSE '1' END),CAST(slices AS TEXT)) numerator
FROM dq_determinant up JOIN dq_determinant down ON down.mask=up.mask AND down.spin=1 CROSS JOIN dq_parameter WHERE up.spin=0;
