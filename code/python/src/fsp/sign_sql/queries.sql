-- ============================================================================
-- queries.sql — the point of the exercise.
--
-- Each query is introduced by a marker line "-- @query <id> <title>" that the
-- runner (run_sign_sql.py) splits on.  Every query carries an ORDER BY so the
-- printed output is deterministic.
--
-- AuthorityEffect: None.  These queries EXHIBIT structure over seeded rows;
-- they prove nothing about physics and derive no hardness result.
-- ============================================================================

-- @query q1 net partition sum per presentation (SUM over signed weights)
-- The signed sum is the collapse observation of rung 6: many weighted paths
-- in, one total out.  Exactness: weights are integer num/den with a COMMON
-- denominator per presentation; distinct_dens is the printed guard (must be
-- 1 for sum_num/common_den to be the exact rational total — SQLite has no
-- rational aggregate, so the guard is shown rather than assumed).
-- Expected: BOTH presentations net to 1/2 — the re-presentation changed the
-- writing, not the thing written.
SELECT
    p.label                              AS presentation,
    SUM(w.num)                           AS sum_num,      -- exact numerator of the net total
    MAX(w.den)                           AS common_den,   -- the shared denominator
    COUNT(DISTINCT w.den)                AS distinct_dens -- exactness guard: must be 1
FROM presentations p
JOIN path_weights w ON w.presentation_id = p.presentation_id
GROUP BY p.presentation_id
ORDER BY p.label;

-- @query q2 L1 mass and sign-problem severity ratio per presentation
-- THE QUERY THAT EXHIBITS CANCELLATION.  The gross L1 mass (SUM of |weight|)
-- and the net signed sum are two different observations of the same rows;
-- their ratio |net|/gross is the sign-problem severity.  With a common
-- denominator the ratio is denominator-free: ratio = |SUM(num)| / SUM(|num|),
-- an exact fraction (printed unreduced — exact nonetheless).
-- Expected: A_frustrated ratio 1/15 (the whisper: gross 15/2 cancels to net
-- 1/2); B_meron_repaired ratio 1/1 (no cancellation — sign-free writing).
SELECT
    p.label                              AS presentation,
    SUM(w.num)                           AS sum_num,      -- net numerator
    SUM(ABS(w.num))                      AS l1_num,       -- gross (L1) numerator
    MAX(w.den)                           AS common_den,   -- shared denominator (cancels in the ratio)
    COUNT(DISTINCT w.den)                AS distinct_dens, -- exactness guard: must be 1
    ABS(SUM(w.num))                      AS ratio_num,    -- exact severity numerator
    SUM(ABS(w.num))                      AS ratio_den,    -- exact severity denominator
    ROUND(CAST(ABS(SUM(w.num)) AS REAL) / SUM(ABS(w.num)), 6)
                                         AS ratio_real,   -- display only; the fraction is the claim
    CASE
        WHEN SUM(ABS(w.num)) = 0 THEN 'undefined_zero_mass'
        ELSE 'defined'
    END                                  AS severity_status -- explicit classification for 0/0 mass
FROM presentations p
JOIN path_weights w ON w.presentation_id = p.presentation_id
GROUP BY p.presentation_id
ORDER BY p.label;

-- @query q3 does a stored sign-free presentation exist? (the re-presentation query)
-- The rung-7 question in EXISTS form: is there a stored presentation of this
-- system in which every weight is non-negative?  Per-presentation verdicts
-- first, then the system-level EXISTS.  Fence: this answers "is one STORED",
-- over declared rows only — it is not a solver, and finding such a
-- presentation in general is exactly what Troyer-Wiese price as NP-hard
-- (external literature; not derived here).
-- Note: A presentation must be nonempty (contain at least one path) to be sign-free.
SELECT
    s.name  AS system_name,
    p.label AS presentation,
    (
        EXISTS (
            SELECT 1 FROM path_weights w
            WHERE w.presentation_id = p.presentation_id
        )
        AND NOT EXISTS (
            SELECT 1 FROM path_weights w
            WHERE w.presentation_id = p.presentation_id AND w.num < 0
        )
    )       AS all_weights_nonnegative,   -- 1 = presentation has paths and every weight is nonnegative
    EXISTS (
        SELECT 1 FROM presentations p2
        WHERE p2.system_id = s.system_id
          AND EXISTS (
              SELECT 1 FROM path_weights w1
              WHERE w1.presentation_id = p2.presentation_id
          )
          AND NOT EXISTS (
              SELECT 1 FROM path_weights w2
              WHERE w2.presentation_id = p2.presentation_id AND w2.num < 0
          )
    )       AS sign_free_presentation_exists  -- 1 = the system HAS a stored nonempty sign-free writing
FROM systems s
JOIN presentations p ON p.system_id = s.system_id
ORDER BY s.name, p.label;

-- @query q4 pricing audit: every admission from the void to rung 7, with its flag
-- The load-bearing discipline query: a recursive CTE climbs the parent chain
-- from the target rung (7, the last walk rung before the declared boundary)
-- down to the void, then lists every admission on that path with its
-- priced/derived flag and price tag.  Anything the walk uses that is not in
-- this list is smuggled; anything priced=1 is a purchase the paper must
-- present as one.  Expected: 17 rows — 10 licensed (priced=0), 7 purchases
-- (priced=1: imports #1..#6 plus the un-numbered asymptotic frame).
WITH RECURSIVE walk(rung_id) AS (
    SELECT rung_id FROM rungs WHERE rung_id = 7
    UNION ALL
    SELECT r.parent_rung_id
    FROM rungs r JOIN walk w ON r.rung_id = w.rung_id
    WHERE r.parent_rung_id IS NOT NULL
)
SELECT
    a.rung_id                       AS rung,
    r.name                          AS rung_name,
    a.name                          AS admission,
    a.kind                          AS kind,
    a.priced                        AS priced,      -- 0 = licensed/derived, 1 = PRICED IMPORT
    COALESCE(a.price_tag, '')       AS price_tag    -- '#1'..'#6', or '' (licensed / un-numbered frame)
FROM admissions a
JOIN walk w  ON w.rung_id = a.rung_id
JOIN rungs r ON r.rung_id = a.rung_id
ORDER BY a.rung_id, a.admission_id;

-- @query q5 obstruction report: what blocks the naive continuation at each rung
-- One row per obstruction, bound to the rung it blocks, with its type and its
-- plain-words terminal.  This is the walk's diagnosis table: each rung's
-- naive continuation fails HERE, and the next rung's admissions are what it
-- costs to get past (or, at rung 8, the walk ends at a declared boundary).
SELECT
    o.rung_id          AS rung,
    r.name             AS rung_name,
    o.obstruction_type AS obstruction_type,
    o.name             AS obstruction,
    o.terminal         AS terminal
FROM obstructions o
JOIN rungs r ON r.rung_id = o.rung_id
ORDER BY o.rung_id, o.obstruction_id;

-- @query q6 the Wheeler-DeWitt boundary row, declared status visible
-- The walk's terminus queried AS DATA: the rung whose standing is
-- 'declared_boundary'.  The standing column is the honesty fence made
-- machine-readable — this row is DECLARED, not derived; it cites the house
-- DeWitt case study (PP/021) and inherits its refusals (continuum REFUSED,
-- constraint-level only).  The joined obstruction is the quotient-without-
-- canonical-section motif the sign-problem rungs instantiate one floor down.
SELECT
    r.rung_id    AS rung,
    r.name       AS rung_name,
    r.standing   AS standing,      -- 'declared_boundary': declared, NOT derived
    r.claim_type AS claim_type,
    o.name       AS obstruction,
    o.terminal   AS terminal,
    r.source     AS source
FROM rungs r
LEFT JOIN obstructions o ON o.rung_id = r.rung_id
WHERE r.standing = 'declared_boundary'
ORDER BY r.rung_id;
