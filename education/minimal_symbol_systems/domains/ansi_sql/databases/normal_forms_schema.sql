-- Relational Normal Forms Schema and BQNF Incremental Maintenance
-- AuthorityEffect: None.

-- ============================================================================
-- 1. 0NF to 1NF: Atomic Domain Normalization
-- ============================================================================

-- 0NF: Non-atomic repeated groups (CSV courses)
CREATE TABLE IF NOT EXISTS student_records_0nf (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    course_list_csv TEXT NOT NULL -- Unparsed non-atomic string
);

-- 1NF: Decomposed into atomic rows with declared candidate key
CREATE TABLE IF NOT EXISTS student_enrollments_1nf (
    student_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    course_code TEXT NOT NULL,
    course_title TEXT NOT NULL,
    instructor_id INTEGER NOT NULL,
    instructor_office TEXT NOT NULL,
    PRIMARY KEY (student_id, course_code)
);

-- ============================================================================
-- 2. 1NF to 2NF: Elimination of Partial Functional Dependencies
-- ============================================================================

-- Partial dependency in 1NF: course_code -> course_title (depends on part of PK)
-- 2NF Decomposition:
CREATE TABLE IF NOT EXISTS courses_2nf (
    course_code TEXT PRIMARY KEY,
    course_title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS student_registrations_2nf (
    student_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    course_code TEXT NOT NULL REFERENCES courses_2nf(course_code),
    instructor_id INTEGER NOT NULL,
    instructor_office TEXT NOT NULL,
    PRIMARY KEY (student_id, course_code)
);

-- ============================================================================
-- 3. 2NF to 3NF & BCNF: Elimination of Transitive Dependencies
-- ============================================================================

-- Transitive dependency: instructor_id -> instructor_office
-- BCNF: Every determinant must be a candidate key
CREATE TABLE IF NOT EXISTS instructors_bcnf (
    instructor_id INTEGER PRIMARY KEY,
    instructor_office TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS course_assignments_bcnf (
    course_code TEXT PRIMARY KEY REFERENCES courses_2nf(course_code),
    instructor_id INTEGER NOT NULL REFERENCES instructors_bcnf(instructor_id)
);

CREATE TABLE IF NOT EXISTS students_bcnf (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS student_courses_bcnf (
    student_id INTEGER NOT NULL REFERENCES students_bcnf(student_id),
    course_code TEXT NOT NULL REFERENCES courses_2nf(course_code),
    PRIMARY KEY (student_id, course_code)
);

-- ============================================================================
-- 4. 4NF: Elimination of Independent Multivalued Dependencies (MVDs)
-- ============================================================================

-- MVD: instructor_id ->> skill | language
-- 4NF Decomposition:
CREATE TABLE IF NOT EXISTS instructor_skills_4nf (
    instructor_id INTEGER NOT NULL REFERENCES instructors_bcnf(instructor_id),
    skill TEXT NOT NULL,
    PRIMARY KEY (instructor_id, skill)
);

CREATE TABLE IF NOT EXISTS instructor_languages_4nf (
    instructor_id INTEGER NOT NULL REFERENCES instructors_bcnf(instructor_id),
    language TEXT NOT NULL,
    PRIMARY KEY (instructor_id, language)
);

-- ============================================================================
-- 5. 5NF (PJNF): Project-Join Higher-Cell Integrity (Shell_2 vs Fill_2)
-- ============================================================================

-- 3-way cyclic relationship: Consultant (C), Company (Co), Product (P)
CREATE TABLE IF NOT EXISTS consulting_fill2 (
    consultant_id TEXT NOT NULL,
    company_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    PRIMARY KEY (consultant_id, company_id, product_id)
);

-- Binary projections:
CREATE VIEW IF NOT EXISTS proj_consultant_company AS
SELECT DISTINCT consultant_id, company_id FROM consulting_fill2;

CREATE VIEW IF NOT EXISTS proj_company_product AS
SELECT DISTINCT company_id, product_id FROM consulting_fill2;

CREATE VIEW IF NOT EXISTS proj_consultant_product AS
SELECT DISTINCT consultant_id, product_id FROM consulting_fill2;

-- Reconstructed boundary shell (Shell_2):
CREATE VIEW IF NOT EXISTS consulting_shell2 AS
SELECT 
    cc.consultant_id,
    cc.company_id,
    cp.product_id
FROM proj_consultant_company cc
JOIN proj_company_product cp ON cc.company_id = cp.company_id
JOIN proj_consultant_product prod 
  ON cc.consultant_id = prod.consultant_id 
 AND cp.product_id = prod.product_id;

-- Spurious tuple query (5NF violation if non-empty):
CREATE VIEW IF NOT EXISTS consulting_spurious_tuples AS
SELECT * FROM consulting_shell2
EXCEPT
SELECT * FROM consulting_fill2;

-- ============================================================================
-- 6. 6NF: Irreducible Binary Decomposition
-- ============================================================================

CREATE TABLE IF NOT EXISTS student_names_6nf (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS student_gpa_6nf (
    student_id INTEGER PRIMARY KEY,
    gpa REAL NOT NULL
);

-- ============================================================================
-- 7. BQNF: Boundary-Quotient Normal Form (Data in Motion under CDC)
-- ============================================================================

CREATE TABLE IF NOT EXISTS base_sales (
    sale_id INTEGER PRIMARY KEY,
    region TEXT NOT NULL,
    amount REAL NOT NULL
);

-- Maintained Materialized Aggregate Cache (Additive SPJA + Non-Invertible Extrema + Quantiles)
CREATE TABLE IF NOT EXISTS region_sales_cache (
    region TEXT PRIMARY KEY,
    total_sales REAL NOT NULL,
    sale_count INTEGER NOT NULL,
    min_amount REAL,
    max_amount REAL,
    median_amount REAL
);

-- CDC Log table (Change Data Capture)
CREATE TABLE IF NOT EXISTS sales_cdc_log (
    cdc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    op_type TEXT NOT NULL CHECK (op_type IN ('INSERT', 'UPDATE', 'DELETE')),
    sale_id INTEGER NOT NULL,
    old_region TEXT,
    new_region TEXT,
    old_amount REAL,
    new_amount REAL,
    processed INTEGER DEFAULT 0
);

-- Auxiliary Priority Queue Cochain for Non-Invertible Aggregates (MIN / MAX)
CREATE TABLE IF NOT EXISTS region_extremum_cochain (
    region TEXT NOT NULL,
    amount REAL NOT NULL,
    frequency INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (region, amount)
);

CREATE INDEX IF NOT EXISTS idx_region_extremum_cochain_lookup 
ON region_extremum_cochain(region, amount ASC);

-- Extrema Repair Audit Log (tracking exact cochain repair vs bounded fallback recomputation)
CREATE TABLE IF NOT EXISTS extrema_repair_log (
    repair_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    op_type TEXT NOT NULL,
    affected_amount REAL,
    is_destructive INTEGER NOT NULL, -- 1 if deleted/updated amount was current min or max
    cochain_available INTEGER NOT NULL, -- 1 if cochain provided next extremum
    terminal_route TEXT NOT NULL, -- 'Repair', 'Recompute', 'Preserve'
    old_min REAL,
    new_min REAL,
    old_max REAL,
    new_max REAL,
    recomputation_fallback_executed INTEGER NOT NULL DEFAULT 0
);

-- Auxiliary Quantile Sketch Cochain for Non-Invertible Quantiles (MEDIAN / Percentiles)
CREATE TABLE IF NOT EXISTS region_quantile_cochain (
    region TEXT NOT NULL,
    bucket_id INTEGER NOT NULL,
    lower_bound REAL NOT NULL,
    upper_bound REAL NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (region, bucket_id)
);

CREATE INDEX IF NOT EXISTS idx_region_quantile_cochain_lookup
ON region_quantile_cochain(region, bucket_id ASC);

-- Quantile Repair Audit Log (tracking epsilon-BQNF sketch tolerance vs bounded fallback recomputation)
CREATE TABLE IF NOT EXISTS quantile_repair_log (
    repair_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    op_type TEXT NOT NULL,
    affected_amount REAL,
    estimated_median REAL,
    true_median REAL,
    error_delta REAL,
    tolerance REAL,
    within_tolerance INTEGER NOT NULL, -- 1 if error_delta <= tolerance
    terminal_route TEXT NOT NULL, -- 'Repair', 'Recompute', 'Preserve'
    recomputation_fallback_executed INTEGER NOT NULL DEFAULT 0
);
