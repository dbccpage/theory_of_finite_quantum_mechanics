-- Exact finite Meron and Hubbard relational evaluator. AuthorityEffect: None.
-- Rational values are reduced TEXT fractions; arithmetic uses qadd/qmul/qsum.
-- Native INTEGER operations act only on bounded counts, masks, and signs.
CREATE TABLE bit(bit INTEGER PRIMARY KEY CHECK(bit IN(0,1)));
INSERT INTO bit VALUES(0),(1);
CREATE TABLE experiment_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE meron_parameter(sites INTEGER,times INTEGER,plaquettes INTEGER,horizontal TEXT);
CREATE TABLE meron_node(node INTEGER PRIMARY KEY,time INTEGER,site INTEGER);
CREATE TABLE meron_plaquette(pid INTEGER PRIMARY KEY,time INTEGER,x INTEGER,y INTEGER,a INTEGER,b INTEGER,c INTEGER,d INTEGER);
CREATE TABLE meron_graph(gid INTEGER PRIMARY KEY,weight TEXT NOT NULL);
CREATE TABLE meron_edge(gid INTEGER,source INTEGER,target INTEGER);
CREATE INDEX meron_edge_source ON meron_edge(gid,source);
CREATE TABLE meron_component(gid INTEGER,node INTEGER,root INTEGER,cluster INTEGER,PRIMARY KEY(gid,node));
CREATE TABLE meron_orientation(gid INTEGER,mask INTEGER,clusters INTEGER,PRIMARY KEY(gid,mask));
CREATE TABLE meron_state(gid INTEGER,mask INTEGER,time INTEGER,state INTEGER,PRIMARY KEY(gid,mask,time));
CREATE TABLE meron_configuration(gid INTEGER,mask INTEGER,sign INTEGER CHECK(sign IN(-1,1)),weight TEXT,PRIMARY KEY(gid,mask));

CREATE VIEW meron_cluster_sign AS
SELECT c.gid,c.cluster,f.sign FROM (SELECT DISTINCT gid,cluster FROM meron_component) c
JOIN meron_configuration f ON f.gid=c.gid AND f.mask=(1 << c.cluster);

-- Validate the character law against CAR signs of all reconstructed occupations.
CREATE VIEW meron_invalid_character AS
SELECT f.gid,f.mask FROM meron_configuration f JOIN meron_cluster_sign c ON c.gid=f.gid
GROUP BY f.gid,f.mask
HAVING f.sign <> CASE WHEN SUM(CASE WHEN c.sign=-1 THEN (f.mask >> c.cluster)&1 ELSE 0 END)%2=0 THEN 1 ELSE -1 END;

CREATE VIEW meron_orbit AS
SELECT g.gid,COUNT(c.cluster) clusters,SUM(c.sign=-1) merons,
qmul(g.weight,CASE WHEN SUM(c.sign=-1)=0 THEN CAST(1 << COUNT(c.cluster) AS TEXT) ELSE '0' END) reduced_weight
FROM meron_graph g JOIN meron_cluster_sign c ON c.gid=g.gid GROUP BY g.gid;

CREATE VIEW meron_cluster_amplitude AS
SELECT c.gid,c.cluster,qdiv(CAST(COUNT(*) AS TEXT),'2') amplitude,s.sign
FROM meron_component c JOIN meron_cluster_sign s ON s.gid=c.gid AND s.cluster=c.cluster GROUP BY c.gid,c.cluster;

CREATE VIEW meron_staggered AS
SELECT f.gid,f.mask,f.sign,f.weight,
qsum(qmul(CASE WHEN (f.mask >> a.cluster)&1 THEN '-1' ELSE '1' END,a.amplitude)) observable
FROM meron_configuration f JOIN meron_cluster_amplitude a ON a.gid=f.gid GROUP BY f.gid,f.mask;

CREATE VIEW meron_squared_orbit AS
SELECT o.gid,qmul(g.weight,qmul(CAST(1 << o.clusters AS TEXT),
 CASE WHEN o.merons=0 THEN (SELECT qsum(qmul(amplitude,amplitude)) FROM meron_cluster_amplitude a WHERE a.gid=o.gid)
 WHEN o.merons=2 THEN (SELECT qmul('2',qmul(a.amplitude,b.amplitude)) FROM meron_cluster_amplitude a
 JOIN meron_cluster_amplitude b ON b.gid=a.gid AND b.cluster>a.cluster AND b.sign=-1
 WHERE a.gid=o.gid AND a.sign=-1)
 ELSE '0' END)) numerator
FROM meron_orbit o JOIN meron_graph g ON g.gid=o.gid;

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
