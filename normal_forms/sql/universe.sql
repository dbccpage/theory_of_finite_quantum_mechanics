-- =====================================================================
-- universe.sql : a relational schema for the repository's facts.
--
-- Dialect : ISO/IEC 9075 SQL:2016, core features only.  CHARACTER
--           VARYING, INTEGER, BOOLEAN, DATE, PRIMARY KEY, FOREIGN KEY,
--           UNIQUE, CHECK, CREATE VIEW with NATURAL JOIN.  No vendor
--           extensions, no vendor-only types, no auto-increment.
-- Status  : a first slice, not the whole universe.  See README.md for
--           what is and is not modelled.
-- Authority effect: None.  Every row is a restatement of a fact that is
--           already in dag/derivation_dag.json, dag/evidence/
--           evidence_map.json, dag/research/*lean_replay*.json or an
--           imported contract under normal_forms/contracts/.  Loading
--           this schema grants no status to any claim.
--
-- Conventions
--   * Every table has a comment block that names the normal form it
--     satisfies and its candidate keys.  "6NF-style" means the relation
--     is irreducible: a key plus at most one independently varying
--     attribute (or a key with no attribute at all), so it has no
--     non-trivial join dependency.  "BCNF" means every non-trivial
--     functional dependency has a superkey as determinant, and the
--     table is not also 6NF-style.  test_universe.py checks the
--     declared keys against the DDL and probes partial dependencies on
--     the loaded data.  Normal-form claims are about the schema design;
--     the data check is a falsification test, not a proof.
--   * An ordered list in the source (for example a node's "lean" array)
--     is stored one row per element with an explicit ordinal, because
--     the source order is part of the source value and duplicates occur.
--   * Optional source fields become optional ROWS, not NULL columns.
--     An empty list and an absent list are both zero rows; the loader
--     and test report where the source distinguishes them.
--   * Column widths: 64 for codes and digests, 128 for identifiers,
--     256 for version strings, 512 for paths and references, 4096 for
--     prose.  test_universe.py checks that no loaded value exceeds its
--     declared width, because SQLite does not enforce it.
-- =====================================================================


-- ---------------------------------------------------------------------
-- A. Vocabularies
-- ---------------------------------------------------------------------

-- TABLE stage
--   Normal form : BCNF
--   Candidate keys: (stage_name); (stage_ordinal)
--   Source      : dag/derivation_dag.json "stages" (array order)
CREATE TABLE stage (
  stage_name    CHARACTER VARYING(64) NOT NULL,
  stage_ordinal INTEGER NOT NULL,
  CONSTRAINT pk_stage PRIMARY KEY (stage_name),
  CONSTRAINT uq_stage_ordinal UNIQUE (stage_ordinal),
  CONSTRAINT ck_stage_ordinal CHECK (stage_ordinal >= 0)
);

-- TABLE node_status_code
--   Normal form : BCNF
--   Candidate keys: (status_code)
--   Source      : dag/derivation_dag.json "status_legend"
CREATE TABLE node_status_code (
  status_code CHARACTER VARYING(64) NOT NULL,
  meaning     CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_node_status_code PRIMARY KEY (status_code)
);

-- TABLE route_status_code
--   Normal form : 6NF-style (key only)
--   Candidate keys: (status_code)
--   Source      : distinct routes[].status in dag/derivation_dag.json.
--                 The source gives no legend for route statuses.
CREATE TABLE route_status_code (
  status_code CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_route_status_code PRIMARY KEY (status_code)
);

-- TABLE record_status_code
--   Normal form : 6NF-style (key only)
--   Candidate keys: (status_code)
--   Source      : distinct records[].record_status.  This vocabulary is
--                 the TFQ record vocabulary, not the node vocabulary.
CREATE TABLE record_status_code (
  status_code CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_record_status_code PRIMARY KEY (status_code)
);

-- TABLE evidence_grade_code
--   Normal form : BCNF
--   Candidate keys: (grade_code)
--   Source      : dag/evidence/evidence_map.json "grade_rules"
CREATE TABLE evidence_grade_code (
  grade_code CHARACTER VARYING(8) NOT NULL,
  rule_text  CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_evidence_grade_code PRIMARY KEY (grade_code)
);

-- TABLE lean_axiom
--   Normal form : 6NF-style (key only)
--   Candidate keys: (axiom_name)
--   Source      : evidence_map.json "allowed_axioms" plus every axiom
--                 named in a loaded replay receipt
CREATE TABLE lean_axiom (
  axiom_name CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_lean_axiom PRIMARY KEY (axiom_name)
);

-- TABLE lean_axiom_allowed
--   Normal form : 6NF-style (key only)
--   Candidate keys: (axiom_name)
--   Source      : evidence_map.json "allowed_axioms"
CREATE TABLE lean_axiom_allowed (
  axiom_name CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_lean_axiom_allowed PRIMARY KEY (axiom_name),
  CONSTRAINT fk_lean_axiom_allowed_axiom FOREIGN KEY (axiom_name)
    REFERENCES lean_axiom (axiom_name)
);


-- ---------------------------------------------------------------------
-- B. Nodes
-- ---------------------------------------------------------------------

-- TABLE node
--   Normal form : 6NF-style (key only)
--   Candidate keys: (node_id)
--   Source      : dag/derivation_dag.json nodes[].id
CREATE TABLE node (
  node_id CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_node PRIMARY KEY (node_id)
);

-- TABLE node_stage
--   Normal form : 6NF-style
--   Candidate keys: (node_id)
--   Source      : nodes[].stage
CREATE TABLE node_stage (
  node_id    CHARACTER VARYING(128) NOT NULL,
  stage_name CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_node_stage PRIMARY KEY (node_id),
  CONSTRAINT fk_node_stage_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT fk_node_stage_stage FOREIGN KEY (stage_name) REFERENCES stage (stage_name)
);

-- TABLE node_status
--   Normal form : 6NF-style
--   Candidate keys: (node_id)
--   Source      : nodes[].status
CREATE TABLE node_status (
  node_id     CHARACTER VARYING(128) NOT NULL,
  status_code CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_node_status PRIMARY KEY (node_id),
  CONSTRAINT fk_node_status_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT fk_node_status_code FOREIGN KEY (status_code) REFERENCES node_status_code (status_code)
);

-- TABLE node_source_status
--   Normal form : 6NF-style
--   Candidate keys: (node_id)
--   Source      : nodes[].source_status.  Free text recording how the
--                 cited source labels the step; it varies independently
--                 of node_status.status_code.
CREATE TABLE node_source_status (
  node_id          CHARACTER VARYING(128) NOT NULL,
  source_status_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_node_source_status PRIMARY KEY (node_id),
  CONSTRAINT fk_node_source_status_node FOREIGN KEY (node_id) REFERENCES node (node_id)
);

-- TABLE node_statement
--   Normal form : 6NF-style
--   Candidate keys: (node_id)
--   Source      : nodes[].statement
CREATE TABLE node_statement (
  node_id        CHARACTER VARYING(128) NOT NULL,
  statement_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_node_statement PRIMARY KEY (node_id),
  CONSTRAINT fk_node_statement_node FOREIGN KEY (node_id) REFERENCES node (node_id)
);

-- TABLE node_bottleneck
--   Normal form : 6NF-style
--   Candidate keys: (node_id)
--   Source      : nodes[].bottleneck
CREATE TABLE node_bottleneck (
  node_id         CHARACTER VARYING(128) NOT NULL,
  bottleneck_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_node_bottleneck PRIMARY KEY (node_id),
  CONSTRAINT fk_node_bottleneck_node FOREIGN KEY (node_id) REFERENCES node (node_id)
);

-- TABLE node_source_ref
--   Normal form : BCNF (ordered list; the value depends on the whole key)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].source
CREATE TABLE node_source_ref (
  node_id    CHARACTER VARYING(128) NOT NULL,
  ordinal    INTEGER NOT NULL,
  source_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_node_source_ref PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_source_ref_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_source_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE node_lean_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].lean.  lean_ref is the source string
--                 "path::symbol" kept atomic; it joins to
--                 lean_declaration through lean_path || '::' || symbol.
CREATE TABLE node_lean_ref (
  node_id  CHARACTER VARYING(128) NOT NULL,
  ordinal  INTEGER NOT NULL,
  lean_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_node_lean_ref PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_lean_ref_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_lean_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE node_rust_ref
--   Normal form : BCNF (ordered list; duplicates occur in the source,
--                 so (node_id, rust_ref) is deliberately not a key)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].rust
CREATE TABLE node_rust_ref (
  node_id  CHARACTER VARYING(128) NOT NULL,
  ordinal  INTEGER NOT NULL,
  rust_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_node_rust_ref PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_rust_ref_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_rust_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE node_python_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].python.  In dag/derivation_dag.json no node
--                 carries a python key, so this table loads empty.  It
--                 exists so the shape matches record_python_ref and a
--                 later DAG that adds the key needs no schema change.
CREATE TABLE node_python_ref (
  node_id    CHARACTER VARYING(128) NOT NULL,
  ordinal    INTEGER NOT NULL,
  python_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_node_python_ref PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_python_ref_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_python_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE node_imported_structure
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].imported_structure
CREATE TABLE node_imported_structure (
  node_id        CHARACTER VARYING(128) NOT NULL,
  ordinal        INTEGER NOT NULL,
  structure_text CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_node_imported_structure PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_imported_structure_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_imported_structure_ordinal CHECK (ordinal >= 0)
);

-- TABLE node_tag
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].tags
CREATE TABLE node_tag (
  node_id  CHARACTER VARYING(128) NOT NULL,
  ordinal  INTEGER NOT NULL,
  tag_text CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_node_tag PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_tag_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_tag_ordinal CHECK (ordinal >= 0)
);

-- TABLE node_see_also
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : nodes[].see_also.  36 nodes carry an explicit empty
--                 list; zero rows cannot tell that from an absent key.
CREATE TABLE node_see_also (
  node_id          CHARACTER VARYING(128) NOT NULL,
  ordinal          INTEGER NOT NULL,
  see_also_node_id CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_node_see_also PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_node_see_also_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT fk_node_see_also_target FOREIGN KEY (see_also_node_id) REFERENCES node (node_id),
  CONSTRAINT ck_node_see_also_ordinal CHECK (ordinal >= 0)
);


-- ---------------------------------------------------------------------
-- C. Routes
-- ---------------------------------------------------------------------

-- TABLE route
--   Normal form : 6NF-style (key only)
--   Candidate keys: (route_id)
--   Source      : dag/derivation_dag.json routes[].id
CREATE TABLE route (
  route_id CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_route PRIMARY KEY (route_id)
);

-- TABLE route_status
--   Normal form : 6NF-style
--   Candidate keys: (route_id)
--   Source      : routes[].status
CREATE TABLE route_status (
  route_id    CHARACTER VARYING(128) NOT NULL,
  status_code CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_route_status PRIMARY KEY (route_id),
  CONSTRAINT fk_route_status_route FOREIGN KEY (route_id) REFERENCES route (route_id),
  CONSTRAINT fk_route_status_code FOREIGN KEY (status_code) REFERENCES route_status_code (status_code)
);

-- TABLE route_input
--   Normal form : BCNF (ordered list)
--   Candidate keys: (route_id, ordinal); (route_id, node_id)
--   Source      : routes[].inputs.  A route requires all of its inputs.
--                 No route lists an input twice, so (route_id, node_id)
--                 is a second key; the loader fails if that stops
--                 being true.
CREATE TABLE route_input (
  route_id CHARACTER VARYING(128) NOT NULL,
  ordinal  INTEGER NOT NULL,
  node_id  CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_route_input PRIMARY KEY (route_id, ordinal),
  CONSTRAINT uq_route_input_node UNIQUE (route_id, node_id),
  CONSTRAINT fk_route_input_route FOREIGN KEY (route_id) REFERENCES route (route_id),
  CONSTRAINT fk_route_input_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_route_input_ordinal CHECK (ordinal >= 0)
);

-- TABLE route_output
--   Normal form : 6NF-style
--   Candidate keys: (route_id)
--   Source      : routes[].output.  Routes with the same output are
--                 alternatives; that is a query, not a constraint.
CREATE TABLE route_output (
  route_id       CHARACTER VARYING(128) NOT NULL,
  output_node_id CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_route_output PRIMARY KEY (route_id),
  CONSTRAINT fk_route_output_route FOREIGN KEY (route_id) REFERENCES route (route_id),
  CONSTRAINT fk_route_output_node FOREIGN KEY (output_node_id) REFERENCES node (node_id)
);

-- TABLE route_source_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (route_id, ordinal)
--   Source      : routes[].source.  Some routes carry an empty list and
--                 some omit the key; both are zero rows here.
CREATE TABLE route_source_ref (
  route_id   CHARACTER VARYING(128) NOT NULL,
  ordinal    INTEGER NOT NULL,
  source_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_route_source_ref PRIMARY KEY (route_id, ordinal),
  CONSTRAINT fk_route_source_ref_route FOREIGN KEY (route_id) REFERENCES route (route_id),
  CONSTRAINT ck_route_source_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE route_mechanism
--   Normal form : 6NF-style
--   Candidate keys: (route_id)
--   Source      : routes[].mechanism (present on some routes only)
CREATE TABLE route_mechanism (
  route_id       CHARACTER VARYING(128) NOT NULL,
  mechanism_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_route_mechanism PRIMARY KEY (route_id),
  CONSTRAINT fk_route_mechanism_route FOREIGN KEY (route_id) REFERENCES route (route_id)
);

-- TABLE route_note
--   Normal form : 6NF-style
--   Candidate keys: (route_id)
--   Source      : routes[].note (present on some routes only)
CREATE TABLE route_note (
  route_id  CHARACTER VARYING(128) NOT NULL,
  note_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_route_note PRIMARY KEY (route_id),
  CONSTRAINT fk_route_note_route FOREIGN KEY (route_id) REFERENCES route (route_id)
);


-- ---------------------------------------------------------------------
-- D. Records (the TFQ records array of dag/derivation_dag.json)
-- ---------------------------------------------------------------------

-- TABLE record
--   Normal form : BCNF (three keys; uuid and local_id are alternate
--                 keys, so every determinant is a superkey)
--   Candidate keys: (record_id); (record_uuid); (local_id)
--   Source      : records[].id, .uuid, .local_id
CREATE TABLE record (
  record_id   CHARACTER VARYING(128) NOT NULL,
  record_uuid CHARACTER VARYING(64) NOT NULL,
  local_id    CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_record PRIMARY KEY (record_id),
  CONSTRAINT uq_record_uuid UNIQUE (record_uuid),
  CONSTRAINT uq_record_local_id UNIQUE (local_id)
);

-- TABLE record_name
--   Normal form : 6NF-style
--   Candidate keys: (record_id)
--   Source      : records[].name
CREATE TABLE record_name (
  record_id   CHARACTER VARYING(128) NOT NULL,
  record_name CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_name PRIMARY KEY (record_id),
  CONSTRAINT fk_record_name_record FOREIGN KEY (record_id) REFERENCES record (record_id)
);

-- TABLE record_summary
--   Normal form : 6NF-style
--   Candidate keys: (record_id)
--   Source      : records[].summary
CREATE TABLE record_summary (
  record_id    CHARACTER VARYING(128) NOT NULL,
  summary_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_record_summary PRIMARY KEY (record_id),
  CONSTRAINT fk_record_summary_record FOREIGN KEY (record_id) REFERENCES record (record_id)
);

-- TABLE record_obligation
--   Normal form : 6NF-style
--   Candidate keys: (record_id)
--   Source      : records[].obligation
CREATE TABLE record_obligation (
  record_id       CHARACTER VARYING(128) NOT NULL,
  obligation_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_record_obligation PRIMARY KEY (record_id),
  CONSTRAINT fk_record_obligation_record FOREIGN KEY (record_id) REFERENCES record (record_id)
);

-- TABLE record_stage
--   Normal form : 6NF-style
--   Candidate keys: (record_id)
--   Source      : records[].stage
CREATE TABLE record_stage (
  record_id  CHARACTER VARYING(128) NOT NULL,
  stage_name CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_record_stage PRIMARY KEY (record_id),
  CONSTRAINT fk_record_stage_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT fk_record_stage_stage FOREIGN KEY (stage_name) REFERENCES stage (stage_name)
);

-- TABLE record_status
--   Normal form : 6NF-style
--   Candidate keys: (record_id)
--   Source      : records[].record_status
CREATE TABLE record_status (
  record_id   CHARACTER VARYING(128) NOT NULL,
  status_code CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_record_status PRIMARY KEY (record_id),
  CONSTRAINT fk_record_status_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT fk_record_status_code FOREIGN KEY (status_code) REFERENCES record_status_code (status_code)
);

-- TABLE record_source_slice
--   Normal form : 6NF-style
--   Candidate keys: (record_id)
--   Source      : records[].source_slice.  The slice does not determine
--                 the stage nor the stage the slice (probed in the tests).
CREATE TABLE record_source_slice (
  record_id    CHARACTER VARYING(128) NOT NULL,
  source_slice CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_record_source_slice PRIMARY KEY (record_id),
  CONSTRAINT fk_record_source_slice_record FOREIGN KEY (record_id) REFERENCES record (record_id)
);

-- TABLE record_parent
--   Normal form : 6NF-style (the root record has no row)
--   Candidate keys: (record_id)
--   Source      : records[].parent_id
CREATE TABLE record_parent (
  record_id        CHARACTER VARYING(128) NOT NULL,
  parent_record_id CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_record_parent PRIMARY KEY (record_id),
  CONSTRAINT fk_record_parent_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT fk_record_parent_parent FOREIGN KEY (parent_record_id) REFERENCES record (record_id)
);

-- TABLE record_coda_atlas_id
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].coda_atlas_ids
CREATE TABLE record_coda_atlas_id (
  record_id     CHARACTER VARYING(128) NOT NULL,
  ordinal       INTEGER NOT NULL,
  coda_atlas_id CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_coda_atlas_id PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_coda_atlas_id_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_coda_atlas_id_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_coda_atlas_path
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].coda_atlas_paths
CREATE TABLE record_coda_atlas_path (
  record_id       CHARACTER VARYING(128) NOT NULL,
  ordinal         INTEGER NOT NULL,
  coda_atlas_path CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_coda_atlas_path PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_coda_atlas_path_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_coda_atlas_path_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_dag_id
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].existing_derivation_dag_ids.  Many of these
--                 name identifiers of an earlier DAG that are not nodes
--                 of this one, so there is deliberately no foreign key
--                 to node.
CREATE TABLE record_dag_id (
  record_id          CHARACTER VARYING(128) NOT NULL,
  ordinal            INTEGER NOT NULL,
  existing_dag_id    CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_record_dag_id PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_dag_id_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_dag_id_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_f004_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].f004_refs
CREATE TABLE record_f004_ref (
  record_id CHARACTER VARYING(128) NOT NULL,
  ordinal   INTEGER NOT NULL,
  f004_ref  CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_f004_ref PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_f004_ref_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_f004_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_lean4_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].lean4
CREATE TABLE record_lean4_ref (
  record_id CHARACTER VARYING(128) NOT NULL,
  ordinal   INTEGER NOT NULL,
  lean4_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_lean4_ref PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_lean4_ref_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_lean4_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_python_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].python.  Some entries are "absent: ..."
--                 notes rather than paths; they are kept as written.
CREATE TABLE record_python_ref (
  record_id  CHARACTER VARYING(128) NOT NULL,
  ordinal    INTEGER NOT NULL,
  python_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_python_ref PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_python_ref_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_python_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_rust_ref
--   Normal form : BCNF (ordered list; the source repeats entries)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].rust
CREATE TABLE record_rust_ref (
  record_id CHARACTER VARYING(128) NOT NULL,
  ordinal   INTEGER NOT NULL,
  rust_ref  CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_rust_ref PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_rust_ref_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_rust_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE record_pfp_review_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (record_id, ordinal)
--   Source      : records[].pfp_review_refs (present on some records only)
CREATE TABLE record_pfp_review_ref (
  record_id      CHARACTER VARYING(128) NOT NULL,
  ordinal        INTEGER NOT NULL,
  pfp_review_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_record_pfp_review_ref PRIMARY KEY (record_id, ordinal),
  CONSTRAINT fk_record_pfp_review_ref_record FOREIGN KEY (record_id) REFERENCES record (record_id),
  CONSTRAINT ck_record_pfp_review_ref_ordinal CHECK (ordinal >= 0)
);


-- ---------------------------------------------------------------------
-- E. Lean evidence (dag/evidence/evidence_map.json and the replay files)
-- ---------------------------------------------------------------------

-- TABLE evidence_grade
--   Normal form : 6NF-style
--   Candidate keys: (node_id)
--   Source      : evidence_map.json nodes[].grade.  A grade describes
--                 what the repository holds for a node; it is not a
--                 verdict on the node's claim.
CREATE TABLE evidence_grade (
  node_id    CHARACTER VARYING(128) NOT NULL,
  grade_code CHARACTER VARYING(8) NOT NULL,
  CONSTRAINT pk_evidence_grade PRIMARY KEY (node_id),
  CONSTRAINT fk_evidence_grade_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT fk_evidence_grade_code FOREIGN KEY (grade_code) REFERENCES evidence_grade_code (grade_code)
);

-- TABLE evidence_fact
--   Normal form : BCNF (the count depends on the whole key)
--   Candidate keys: (node_id, fact_name)
--   Source      : evidence_map.json nodes[].facts
CREATE TABLE evidence_fact (
  node_id    CHARACTER VARYING(128) NOT NULL,
  fact_name  CHARACTER VARYING(64) NOT NULL,
  fact_count INTEGER NOT NULL,
  CONSTRAINT pk_evidence_fact PRIMARY KEY (node_id, fact_name),
  CONSTRAINT fk_evidence_fact_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT ck_evidence_fact_name CHECK (fact_name IN (
    'cited_code_files_not_tests', 'counted_files', 'lean_receipt_backed',
    'qualifying_reviews', 'runnable_tests', 'symbols_found')),
  CONSTRAINT ck_evidence_fact_count CHECK (fact_count >= 0)
);

-- TABLE evidence_file
--   Normal form : BCNF
--   Candidate keys: (evidence_path)
--   Source      : evidence_map.json "files".  sha256_basis says whether
--                 the digest is over the raw bytes or over LF-normalised
--                 text.
CREATE TABLE evidence_file (
  evidence_path CHARACTER VARYING(512) NOT NULL,
  sha256        CHARACTER VARYING(64) NOT NULL,
  sha256_basis  CHARACTER VARYING(32) NOT NULL,
  size_bytes    INTEGER NOT NULL,
  CONSTRAINT pk_evidence_file PRIMARY KEY (evidence_path),
  CONSTRAINT ck_evidence_file_basis CHECK (sha256_basis IN ('bytes', 'lf-normalised')),
  CONSTRAINT ck_evidence_file_size CHECK (size_bytes >= 0)
);

-- TABLE lean_file
--   Normal form : 6NF-style
--   Candidate keys: (lean_path)
--   Source      : evidence_map.json nodes[].items[] with kind
--                 "lean_decl".  resolution is a property of the file:
--                 'present' means the file exists in this checkout;
--                 'external_unresolved' and 'missing' mean it does not.
--                 (file_exists would be a function of resolution and is
--                 not stored.)
CREATE TABLE lean_file (
  lean_path  CHARACTER VARYING(512) NOT NULL,
  resolution CHARACTER VARYING(32) NOT NULL,
  CONSTRAINT pk_lean_file PRIMARY KEY (lean_path),
  CONSTRAINT ck_lean_file_resolution CHECK (resolution IN ('present', 'external_unresolved', 'missing'))
);

-- TABLE lean_file_replay
--   Normal form : 6NF-style
--   Candidate keys: (lean_path)
--   Source      : the same items' "replay" field.  'verified' means a
--                 current replay receipt names the file; 'none' means
--                 the file exists with no such receipt; 'n/a' is used
--                 when the file is not in this checkout.
CREATE TABLE lean_file_replay (
  lean_path     CHARACTER VARYING(512) NOT NULL,
  replay_status CHARACTER VARYING(16) NOT NULL,
  CONSTRAINT pk_lean_file_replay PRIMARY KEY (lean_path),
  CONSTRAINT fk_lean_file_replay_file FOREIGN KEY (lean_path) REFERENCES lean_file (lean_path),
  CONSTRAINT ck_lean_file_replay_status CHECK (replay_status IN ('verified', 'none', 'n/a'))
);

-- TABLE lean_declaration
--   Normal form : 6NF-style (key only)
--   Candidate keys: (lean_path, symbol)
--   Source      : evidence_map.json lean_decl items that name a symbol.
--                 The same symbol name occurs under several paths, so
--                 the path is part of the key.
CREATE TABLE lean_declaration (
  lean_path CHARACTER VARYING(512) NOT NULL,
  symbol    CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_lean_declaration PRIMARY KEY (lean_path, symbol),
  CONSTRAINT fk_lean_declaration_file FOREIGN KEY (lean_path) REFERENCES lean_file (lean_path)
);

-- TABLE lean_declaration_scan
--   Normal form : 6NF-style
--   Candidate keys: (lean_path, symbol)
--   Source      : items' symbol_declared and symbol_exists.  Rows exist
--                 only for declarations whose file is in this checkout;
--                 for the others the source gives null and no row is
--                 stored.
CREATE TABLE lean_declaration_scan (
  lean_path       CHARACTER VARYING(512) NOT NULL,
  symbol          CHARACTER VARYING(512) NOT NULL,
  symbol_declared BOOLEAN NOT NULL,
  symbol_exists   BOOLEAN NOT NULL,
  CONSTRAINT pk_lean_declaration_scan PRIMARY KEY (lean_path, symbol),
  CONSTRAINT fk_lean_declaration_scan_decl FOREIGN KEY (lean_path, symbol)
    REFERENCES lean_declaration (lean_path, symbol),
  CONSTRAINT ck_lean_declaration_scan_declared CHECK (symbol_declared IN (TRUE, FALSE)),
  CONSTRAINT ck_lean_declaration_scan_exists CHECK (symbol_exists IN (TRUE, FALSE))
);

-- TABLE lean_declaration_listing
--   Normal form : BCNF (decl_listed and decl_ambiguous have no
--                 dependency between them in the data)
--   Candidate keys: (lean_path, symbol)
--   Source      : items' decl_listed and decl_ambiguous
CREATE TABLE lean_declaration_listing (
  lean_path      CHARACTER VARYING(512) NOT NULL,
  symbol         CHARACTER VARYING(512) NOT NULL,
  decl_listed    BOOLEAN NOT NULL,
  decl_ambiguous BOOLEAN NOT NULL,
  CONSTRAINT pk_lean_declaration_listing PRIMARY KEY (lean_path, symbol),
  CONSTRAINT fk_lean_declaration_listing_decl FOREIGN KEY (lean_path, symbol)
    REFERENCES lean_declaration (lean_path, symbol),
  CONSTRAINT ck_lean_declaration_listing_listed CHECK (decl_listed IN (TRUE, FALSE)),
  CONSTRAINT ck_lean_declaration_listing_ambiguous CHECK (decl_ambiguous IN (TRUE, FALSE))
);

-- TABLE replay_receipt
--   Normal form : BCNF (one receipt file; every attribute is a fact of
--                 the file, none determines another)
--   Candidate keys: (receipt_file)
--   Source      : evidence_map.json receipts[] grouped by receipt_file.
--                 The toolchain string in the source is the numeric part
--                 of lean_version and is not stored again.
CREATE TABLE replay_receipt (
  receipt_file        CHARACTER VARYING(512) NOT NULL,
  receipt_file_sha256 CHARACTER VARYING(64) NOT NULL,
  checked_at          DATE NOT NULL,
  lean_version        CHARACTER VARYING(256) NOT NULL,
  mathlib_source_sha  CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_replay_receipt PRIMARY KEY (receipt_file)
);

-- TABLE lean_module
--   Normal form : 6NF-style
--   Candidate keys: (lean_module_name); (lean_path)
--   Source      : receipts[].module and .path.  The same module is
--                 replayed in several receipt files, so the path is a
--                 fact of the module, not of the receipt.
CREATE TABLE lean_module (
  lean_module_name CHARACTER VARYING(128) NOT NULL,
  lean_path        CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_lean_module PRIMARY KEY (lean_module_name),
  CONSTRAINT uq_lean_module_path UNIQUE (lean_path)
);

-- TABLE lean_module_node
--   Normal form : 6NF-style
--   Candidate keys: (lean_module_name)
--   Source      : receipts[].dag_node.  Receipts of the tensor
--                 validation files carry no DAG node, so those modules
--                 have no row.
CREATE TABLE lean_module_node (
  lean_module_name CHARACTER VARYING(128) NOT NULL,
  node_id          CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_lean_module_node PRIMARY KEY (lean_module_name),
  CONSTRAINT fk_lean_module_node_module FOREIGN KEY (lean_module_name)
    REFERENCES lean_module (lean_module_name),
  CONSTRAINT fk_lean_module_node_node FOREIGN KEY (node_id) REFERENCES node (node_id)
);

-- TABLE receipt_module
--   Normal form : BCNF
--   Candidate keys: (receipt_file, lean_module_name); (receipt_file, file_index)
--   Source      : evidence_map.json receipts[]: one module result inside
--                 a receipt file.  decl_count is the recorded count; the
--                 tests compare it with the number of itemised
--                 declarations where the file itemises them.
CREATE TABLE receipt_module (
  receipt_file     CHARACTER VARYING(512) NOT NULL,
  lean_module_name CHARACTER VARYING(128) NOT NULL,
  file_index       INTEGER NOT NULL,
  recorded_sha256  CHARACTER VARYING(64) NOT NULL,
  exit_code        INTEGER NOT NULL,
  decl_count       INTEGER NOT NULL,
  CONSTRAINT pk_receipt_module PRIMARY KEY (receipt_file, lean_module_name),
  CONSTRAINT uq_receipt_module_index UNIQUE (receipt_file, file_index),
  CONSTRAINT fk_receipt_module_receipt FOREIGN KEY (receipt_file)
    REFERENCES replay_receipt (receipt_file),
  CONSTRAINT fk_receipt_module_module FOREIGN KEY (lean_module_name)
    REFERENCES lean_module (lean_module_name),
  CONSTRAINT ck_receipt_module_index CHECK (file_index >= 0),
  CONSTRAINT ck_receipt_module_count CHECK (decl_count >= 0)
);

-- TABLE receipt_module_build
--   Normal form : 6NF-style
--   Candidate keys: (receipt_file, lean_module_name)
--   Source      : receipts[].built_successfully.  Only the frontier
--                 targets file records this flag; the other receipt
--                 files give null and so have no row.
CREATE TABLE receipt_module_build (
  receipt_file       CHARACTER VARYING(512) NOT NULL,
  lean_module_name   CHARACTER VARYING(128) NOT NULL,
  built_successfully BOOLEAN NOT NULL,
  CONSTRAINT pk_receipt_module_build PRIMARY KEY (receipt_file, lean_module_name),
  CONSTRAINT fk_receipt_module_build_module FOREIGN KEY (receipt_file, lean_module_name)
    REFERENCES receipt_module (receipt_file, lean_module_name),
  CONSTRAINT ck_receipt_module_build CHECK (built_successfully IN (TRUE, FALSE))
);

-- TABLE receipt_module_source_unchanged
--   Normal form : 6NF-style
--   Candidate keys: (receipt_file, lean_module_name)
--   Source      : receipts[].source_unchanged_during_build.  One replay
--                 receipt omits the flag; that module has no row.
CREATE TABLE receipt_module_source_unchanged (
  receipt_file                  CHARACTER VARYING(512) NOT NULL,
  lean_module_name              CHARACTER VARYING(128) NOT NULL,
  source_unchanged_during_build BOOLEAN NOT NULL,
  CONSTRAINT pk_receipt_module_source_unchanged PRIMARY KEY (receipt_file, lean_module_name),
  CONSTRAINT fk_receipt_module_source_unchanged_module FOREIGN KEY (receipt_file, lean_module_name)
    REFERENCES receipt_module (receipt_file, lean_module_name),
  CONSTRAINT ck_receipt_module_source_unchanged CHECK (source_unchanged_during_build IN (TRUE, FALSE))
);

-- TABLE receipt_module_audit
--   Normal form : BCNF (four audit flags of one module result)
--   Candidate keys: (receipt_file, lean_module_name)
--   Source      : receipts[] flags of the same names.  These four are
--                 present on every receipt.  source_unchanged_during_build
--                 is the optional-row table above.
CREATE TABLE receipt_module_audit (
  receipt_file          CHARACTER VARYING(512) NOT NULL,
  lean_module_name      CHARACTER VARYING(128) NOT NULL,
  admission_scan_passed BOOLEAN NOT NULL,
  axiom_audit_passed    BOOLEAN NOT NULL,
  axioms_itemised       BOOLEAN NOT NULL,
  axioms_standard       BOOLEAN NOT NULL,
  CONSTRAINT pk_receipt_module_audit PRIMARY KEY (receipt_file, lean_module_name),
  CONSTRAINT fk_receipt_module_audit_module FOREIGN KEY (receipt_file, lean_module_name)
    REFERENCES receipt_module (receipt_file, lean_module_name),
  CONSTRAINT ck_receipt_module_audit_b CHECK (admission_scan_passed IN (TRUE, FALSE)),
  CONSTRAINT ck_receipt_module_audit_c CHECK (axiom_audit_passed IN (TRUE, FALSE)),
  CONSTRAINT ck_receipt_module_audit_d CHECK (axioms_itemised IN (TRUE, FALSE)),
  CONSTRAINT ck_receipt_module_audit_e CHECK (axioms_standard IN (TRUE, FALSE))
);

-- TABLE receipt_declaration
--   Normal form : 6NF-style (key only)
--   Candidate keys: (receipt_file, lean_module_name, declaration)
--   Source      : the "axioms" object of each module result in
--                 dag/research/*lean_replay*.json, one row per declaration
--                 name, including declarations that use no axiom.
--                 Results sit at lean_replay.results, or at the top level
--                 when a campaign receipt has no lean_replay object.
CREATE TABLE receipt_declaration (
  receipt_file     CHARACTER VARYING(512) NOT NULL,
  lean_module_name CHARACTER VARYING(128) NOT NULL,
  declaration      CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_receipt_declaration PRIMARY KEY (receipt_file, lean_module_name, declaration),
  CONSTRAINT fk_receipt_declaration_module FOREIGN KEY (receipt_file, lean_module_name)
    REFERENCES receipt_module (receipt_file, lean_module_name)
);

-- TABLE receipt_axiom
--   Normal form : 6NF-style (key only; one row per declaration x axiom)
--   Candidate keys: (receipt_file, lean_module_name, declaration, axiom_name)
--   Source      : the axiom arrays of the same objects
CREATE TABLE receipt_axiom (
  receipt_file     CHARACTER VARYING(512) NOT NULL,
  lean_module_name CHARACTER VARYING(128) NOT NULL,
  declaration      CHARACTER VARYING(512) NOT NULL,
  axiom_name       CHARACTER VARYING(128) NOT NULL,
  CONSTRAINT pk_receipt_axiom PRIMARY KEY (receipt_file, lean_module_name, declaration, axiom_name),
  CONSTRAINT fk_receipt_axiom_declaration FOREIGN KEY (receipt_file, lean_module_name, declaration)
    REFERENCES receipt_declaration (receipt_file, lean_module_name, declaration),
  CONSTRAINT fk_receipt_axiom_axiom FOREIGN KEY (axiom_name) REFERENCES lean_axiom (axiom_name)
);


-- ---------------------------------------------------------------------
-- F. Reviews (nodes[].pfp_review)
-- ---------------------------------------------------------------------

-- TABLE pfp_review_file
--   Normal form : BCNF
--   Candidate keys: (review_path)
--   Source      : pfp_review.review and pfp_review.review_sha256.  The
--                 digest is a fact of the review file, so it lives here
--                 and not in pfp_review.
CREATE TABLE pfp_review_file (
  review_path   CHARACTER VARYING(512) NOT NULL,
  review_sha256 CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_pfp_review_file PRIMARY KEY (review_path)
);

-- TABLE pfp_review
--   Normal form : BCNF
--   Candidate keys: (node_id)
--   Source      : pfp_review.review, .verdict, .scope_effect, .reason.
--                 One review per node in the source.
CREATE TABLE pfp_review (
  node_id          CHARACTER VARYING(128) NOT NULL,
  review_path      CHARACTER VARYING(512) NOT NULL,
  verdict          CHARACTER VARYING(128) NOT NULL,
  scope_effect     CHARACTER VARYING(64) NOT NULL,
  reason_text      CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_pfp_review PRIMARY KEY (node_id),
  CONSTRAINT fk_pfp_review_node FOREIGN KEY (node_id) REFERENCES node (node_id),
  CONSTRAINT fk_pfp_review_file FOREIGN KEY (review_path) REFERENCES pfp_review_file (review_path)
);

-- TABLE pfp_review_claim
--   Normal form : BCNF (the three claim-hygiene texts of one review)
--   Candidate keys: (node_id)
--   Source      : pfp_review.narrowest_claim, .does_not_support, .next_test
CREATE TABLE pfp_review_claim (
  node_id                CHARACTER VARYING(128) NOT NULL,
  narrowest_claim_text   CHARACTER VARYING(4096) NOT NULL,
  does_not_support_text  CHARACTER VARYING(4096) NOT NULL,
  next_test_text         CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_pfp_review_claim PRIMARY KEY (node_id),
  CONSTRAINT fk_pfp_review_claim_review FOREIGN KEY (node_id) REFERENCES pfp_review (node_id)
);

-- TABLE pfp_review_prior
--   Normal form : BCNF (the node's state before the review)
--   Candidate keys: (node_id)
--   Source      : pfp_review.prior_status, .prior_statement, .prior_bottleneck
CREATE TABLE pfp_review_prior (
  node_id               CHARACTER VARYING(128) NOT NULL,
  prior_status_code     CHARACTER VARYING(64) NOT NULL,
  prior_statement_text  CHARACTER VARYING(4096) NOT NULL,
  prior_bottleneck_text CHARACTER VARYING(4096) NOT NULL,
  CONSTRAINT pk_pfp_review_prior PRIMARY KEY (node_id),
  CONSTRAINT fk_pfp_review_prior_review FOREIGN KEY (node_id) REFERENCES pfp_review (node_id),
  CONSTRAINT fk_pfp_review_prior_status FOREIGN KEY (prior_status_code) REFERENCES node_status_code (status_code)
);

-- TABLE pfp_review_ref
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : pfp_review.review_refs
CREATE TABLE pfp_review_ref (
  node_id    CHARACTER VARYING(128) NOT NULL,
  ordinal    INTEGER NOT NULL,
  review_ref CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_pfp_review_ref PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_pfp_review_ref_review FOREIGN KEY (node_id) REFERENCES pfp_review (node_id),
  CONSTRAINT ck_pfp_review_ref_ordinal CHECK (ordinal >= 0)
);

-- TABLE pfp_review_superseded_by
--   Normal form : BCNF (ordered list)
--   Candidate keys: (node_id, ordinal)
--   Source      : pfp_review.superseded_by.  The entries are identifiers
--                 of superseded items as written in the review; they are
--                 not all node identifiers, so there is no foreign key
--                 to node.
CREATE TABLE pfp_review_superseded_by (
  node_id       CHARACTER VARYING(128) NOT NULL,
  ordinal       INTEGER NOT NULL,
  superseded_by CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_pfp_review_superseded_by PRIMARY KEY (node_id, ordinal),
  CONSTRAINT fk_pfp_review_superseded_by_review FOREIGN KEY (node_id) REFERENCES pfp_review (node_id),
  CONSTRAINT ck_pfp_review_superseded_by_ordinal CHECK (ordinal >= 0)
);

-- TABLE pfp_review_prior_route_status
--   Normal form : BCNF (the prior status depends on the whole key)
--   Candidate keys: (node_id, route_id)
--   Source      : pfp_review.prior_route_status (a route-id -> status object)
CREATE TABLE pfp_review_prior_route_status (
  node_id           CHARACTER VARYING(128) NOT NULL,
  route_id          CHARACTER VARYING(128) NOT NULL,
  prior_status_code CHARACTER VARYING(64) NOT NULL,
  CONSTRAINT pk_pfp_review_prior_route_status PRIMARY KEY (node_id, route_id),
  CONSTRAINT fk_pfp_review_prior_route_status_review FOREIGN KEY (node_id) REFERENCES pfp_review (node_id),
  CONSTRAINT fk_pfp_review_prior_route_status_route FOREIGN KEY (route_id) REFERENCES route (route_id),
  CONSTRAINT fk_pfp_review_prior_route_status_code FOREIGN KEY (prior_status_code)
    REFERENCES route_status_code (status_code)
);


-- ---------------------------------------------------------------------
-- G. Imported normal-form contracts (normal_forms/contracts/)
--    Authority effect: None.  These rows describe imported documents.
-- ---------------------------------------------------------------------

-- TABLE nf_contract
--   Normal form : BCNF
--   Candidate keys: (nf_id)
--   Source      : identity.id, .name, .short_name, .family,
--                 classification.hierarchy_level, purpose.excludes_anomaly,
--                 purpose.preserves_invariant, plus index.yaml for
--                 index_status.
--                 category is derived by the loader, not read from a
--                 field: 'true_normal_form' when the contract's
--                 quadrilateral says qualifies_as_true_normal_form is
--                 true; 'extended_form_contract' when it says
--                 qualifies_as_extended_form is true or
--                 nf_domain_index.yaml lists it so; 'not_true_normal_form'
--                 when it says false with no extended claim; otherwise
--                 'unstated'.  index_status is the status in the source
--                 index.yaml, which can disagree with the contract's own
--                 contract_status (see nf_contract_status).
CREATE TABLE nf_contract (
  nf_id               CHARACTER VARYING(128) NOT NULL,
  name                CHARACTER VARYING(256) NOT NULL,
  short_name          CHARACTER VARYING(64) NOT NULL,
  family              CHARACTER VARYING(64) NOT NULL,
  category            CHARACTER VARYING(32) NOT NULL,
  hierarchy_level     CHARACTER VARYING(64) NOT NULL,
  index_status        CHARACTER VARYING(16) NOT NULL,
  excludes_anomaly    CHARACTER VARYING(1024) NOT NULL,
  preserves_invariant CHARACTER VARYING(1024) NOT NULL,
  CONSTRAINT pk_nf_contract PRIMARY KEY (nf_id),
  CONSTRAINT ck_nf_contract_category CHECK (category IN
    ('true_normal_form', 'extended_form_contract', 'not_true_normal_form', 'unstated')),
  CONSTRAINT ck_nf_contract_index_status CHECK (index_status IN ('active', 'draft'))
);

-- TABLE nf_contract_status
--   Normal form : 6NF-style
--   Candidate keys: (nf_id)
--   Source      : identity.contract_status.  One contract
--                 (nf.operational.schema-totality) omits the field, so
--                 it has no row.
CREATE TABLE nf_contract_status (
  nf_id           CHARACTER VARYING(128) NOT NULL,
  contract_status CHARACTER VARYING(16) NOT NULL,
  CONSTRAINT pk_nf_contract_status PRIMARY KEY (nf_id),
  CONSTRAINT fk_nf_contract_status_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id),
  CONSTRAINT ck_nf_contract_status CHECK (contract_status IN ('draft', 'active', 'deprecated'))
);

-- TABLE nf_verification_status
--   Normal form : 6NF-style
--   Candidate keys: (nf_id)
--   Source      : identity.verification_status (omitted by one contract)
CREATE TABLE nf_verification_status (
  nf_id               CHARACTER VARYING(128) NOT NULL,
  verification_status CHARACTER VARYING(32) NOT NULL,
  CONSTRAINT pk_nf_verification_status PRIMARY KEY (nf_id),
  CONSTRAINT fk_nf_verification_status_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id),
  CONSTRAINT ck_nf_verification_status CHECK (verification_status IN ('absent', 'executable', 'machine_checked'))
);

-- TABLE nf_theory_status
--   Normal form : 6NF-style
--   Candidate keys: (nf_id)
--   Source      : identity.theory_status (omitted by one contract).  No
--                 CHECK: three contracts use 'admitted', which is not in
--                 the source schema's enum, and the value is kept as
--                 written.
CREATE TABLE nf_theory_status (
  nf_id         CHARACTER VARYING(128) NOT NULL,
  theory_status CHARACTER VARYING(32) NOT NULL,
  CONSTRAINT pk_nf_theory_status PRIMARY KEY (nf_id),
  CONSTRAINT fk_nf_theory_status_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id)
);

-- TABLE nf_work
--   Normal form : BCNF
--   Candidate keys: (citation_work)
--   Source      : definition.citation (authors or author, year, work) of
--                 the classical contracts.  Several contracts cite the
--                 same work, and the data shows work -> authors, year;
--                 keeping all three in nf_citation put that dependency
--                 on a non-key determinant, so the work is its own
--                 relation.  This takes the title as the identifier of a
--                 work, which holds in the imported set; the loader fails
--                 if two contracts give one title different authors or
--                 years.
CREATE TABLE nf_work (
  citation_work    CHARACTER VARYING(512) NOT NULL,
  citation_authors CHARACTER VARYING(512) NOT NULL,
  citation_year    INTEGER NOT NULL,
  CONSTRAINT pk_nf_work PRIMARY KEY (citation_work)
);

-- TABLE nf_citation
--   Normal form : 6NF-style
--   Candidate keys: (nf_id)
--   Source      : definition.citation of the contract (one work each).
--                 Only the classical contracts carry one.
CREATE TABLE nf_citation (
  nf_id         CHARACTER VARYING(128) NOT NULL,
  citation_work CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_nf_citation PRIMARY KEY (nf_id),
  CONSTRAINT fk_nf_citation_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id),
  CONSTRAINT fk_nf_citation_work FOREIGN KEY (citation_work) REFERENCES nf_work (citation_work)
);

-- TABLE nf_citation_label
--   Normal form : 6NF-style
--   Candidate keys: (nf_id)
--   Source      : definition.citation.label, used by nf.classical.0nf
--                 in place of a bibliographic citation
CREATE TABLE nf_citation_label (
  nf_id          CHARACTER VARYING(128) NOT NULL,
  citation_label CHARACTER VARYING(512) NOT NULL,
  CONSTRAINT pk_nf_citation_label PRIMARY KEY (nf_id),
  CONSTRAINT fk_nf_citation_label_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id)
);

-- TABLE nf_non_claim
--   Normal form : BCNF (ordered list)
--   Candidate keys: (nf_id, ordinal)
--   Source      : purpose.non_claims
CREATE TABLE nf_non_claim (
  nf_id          CHARACTER VARYING(128) NOT NULL,
  ordinal        INTEGER NOT NULL,
  non_claim_text CHARACTER VARYING(1024) NOT NULL,
  CONSTRAINT pk_nf_non_claim PRIMARY KEY (nf_id, ordinal),
  CONSTRAINT fk_nf_non_claim_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id),
  CONSTRAINT ck_nf_non_claim_ordinal CHECK (ordinal >= 0)
);

-- TABLE nf_source_file
--   Normal form : BCNF
--   Candidate keys: (nf_id); (source_relative_path); (sha256)
--   Source      : normal_forms/contracts/PROVENANCE.json entries of kind
--                 "contract"
CREATE TABLE nf_source_file (
  nf_id                CHARACTER VARYING(128) NOT NULL,
  source_relative_path CHARACTER VARYING(512) NOT NULL,
  sha256               CHARACTER VARYING(64) NOT NULL,
  size_bytes           INTEGER NOT NULL,
  CONSTRAINT pk_nf_source_file PRIMARY KEY (nf_id),
  CONSTRAINT uq_nf_source_file_path UNIQUE (source_relative_path),
  CONSTRAINT uq_nf_source_file_sha UNIQUE (sha256),
  CONSTRAINT fk_nf_source_file_contract FOREIGN KEY (nf_id) REFERENCES nf_contract (nf_id)
);


-- ---------------------------------------------------------------------
-- H. Views: the natural-join reconstructions used by the lossless test
--    Each is a NATURAL JOIN of the 1:1 relations above; the shared
--    column is the key.  List-valued fields are reassembled from the
--    ordinal tables by the caller, in ordinal order.
-- ---------------------------------------------------------------------

CREATE VIEW node_core AS
  SELECT node_id, stage_name, status_code, source_status_text,
         statement_text, bottleneck_text
  FROM node
  NATURAL JOIN node_stage
  NATURAL JOIN node_status
  NATURAL JOIN node_source_status
  NATURAL JOIN node_statement
  NATURAL JOIN node_bottleneck;

CREATE VIEW route_core AS
  SELECT route_id, status_code, output_node_id
  FROM route
  NATURAL JOIN route_status
  NATURAL JOIN route_output;

CREATE VIEW record_core AS
  SELECT record_id, record_uuid, local_id, record_name, summary_text,
         obligation_text, stage_name, status_code, source_slice
  FROM record
  NATURAL JOIN record_name
  NATURAL JOIN record_summary
  NATURAL JOIN record_obligation
  NATURAL JOIN record_stage
  NATURAL JOIN record_status
  NATURAL JOIN record_source_slice;
