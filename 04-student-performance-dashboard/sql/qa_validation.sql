PRAGMA foreign_keys = ON;


-- ============================================================
-- QA-DB-001: Validate attempt-to-student referential integrity
-- Expected: 0 rows
-- ============================================================

SELECT
    a.attempt_id,
    a.student_id
FROM attempts a
LEFT JOIN students s
    ON a.student_id = s.student_id
WHERE s.student_id IS NULL;


-- ============================================================
-- QA-DB-002: Every test must contain exactly 180 questions
-- Expected: 0 rows
-- ============================================================

SELECT
    t.test_id,
    t.test_name,
    COUNT(q.question_id) AS question_count
FROM tests t
LEFT JOIN questions q
    ON t.test_id = q.test_id
GROUP BY
    t.test_id,
    t.test_name
HAVING COUNT(q.question_id) <> 180;


-- ============================================================
-- QA-DB-003: Every question must carry exactly 4 marks
-- Expected: 0 rows
-- ============================================================

SELECT
    question_id,
    test_id,
    marks
FROM questions
WHERE marks <> 4;


-- ============================================================
-- QA-DB-004: Test total marks must equal 720
-- 180 questions × 4 marks = 720
-- Expected: 0 rows
-- ============================================================

SELECT
    t.test_id,
    t.test_name,
    t.total_marks,
    COUNT(q.question_id) * 4 AS calculated_total_marks
FROM tests t
JOIN questions q
    ON t.test_id = q.test_id
GROUP BY
    t.test_id,
    t.test_name,
    t.total_marks
HAVING t.total_marks <> COUNT(q.question_id) * 4;


-- ============================================================
-- QA-DB-005: Every attempt must contain exactly 180 answers
-- Expected: 0 rows
-- ============================================================

SELECT
    a.attempt_id,
    s.student_name,
    t.test_name,
    COUNT(aa.answer_id) AS answer_count
FROM attempts a
JOIN students s
    ON a.student_id = s.student_id
JOIN tests t
    ON a.test_id = t.test_id
LEFT JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id
GROUP BY
    a.attempt_id,
    s.student_name,
    t.test_name
HAVING COUNT(aa.answer_id) <> 180;


-- ============================================================
-- QA-DB-006: Validate +4 / -1 / 0 scoring
--
-- Correct     = +4
-- Wrong       = -1
-- Unattempted =  0
--
-- Expected: 0 rows
-- ============================================================

SELECT
    a.attempt_id,
    s.student_name,
    t.test_name,
    a.score AS stored_score,

    SUM(
        CASE
            WHEN aa.is_correct = 1 THEN 4
            WHEN aa.is_correct = 0
                 AND aa.selected_answer IS NOT NULL THEN -1
            ELSE 0
        END
    ) AS calculated_score

FROM attempts a
JOIN students s
    ON a.student_id = s.student_id
JOIN tests t
    ON a.test_id = t.test_id
JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id

GROUP BY
    a.attempt_id,
    s.student_name,
    t.test_name,
    a.score

HAVING a.score <> calculated_score;


-- ============================================================
-- QA-DB-007: Validate attempt total marks
-- Expected: 0 rows
-- ============================================================

SELECT
    attempt_id,
    student_id,
    test_id,
    total_marks
FROM attempts
WHERE total_marks <> 720;


-- ============================================================
-- QA-DB-008: Validate pass/fail status
--
-- Score >= 360 = passed
-- Score < 360  = failed
--
-- Expected: 0 rows
-- ============================================================

SELECT
    a.attempt_id,
    s.student_name,
    t.test_name,
    a.score,
    t.pass_marks,
    a.status,
    CASE
        WHEN a.score >= t.pass_marks THEN 'passed'
        ELSE 'failed'
    END AS calculated_status

FROM attempts a

JOIN students s
    ON a.student_id = s.student_id

JOIN tests t
    ON a.test_id = t.test_id

WHERE a.status <>
    CASE
        WHEN a.score >= t.pass_marks THEN 'passed'
        ELSE 'failed'
    END;


-- ============================================================
-- QA-DB-009: Validate answer-level scoring
--
-- Correct     = 4
-- Wrong       = -1
-- Unattempted = 0
--
-- Expected: 0 rows
-- ============================================================

SELECT
    answer_id,
    attempt_id,
    question_id,
    is_correct,
    selected_answer,
    marks_obtained

FROM attempt_answers

WHERE
    (is_correct = 1 AND marks_obtained <> 4)

    OR

    (
        is_correct = 0
        AND selected_answer IS NOT NULL
        AND marks_obtained <> -1
    )

    OR

    (
        selected_answer IS NULL
        AND marks_obtained <> 0
    );


-- ============================================================
-- QA-DB-010: Validate question belongs to attempt's test
-- Expected: 0 rows
-- ============================================================

SELECT
    aa.answer_id,
    aa.attempt_id,
    aa.question_id,
    a.test_id AS attempt_test_id,
    q.test_id AS question_test_id

FROM attempt_answers aa

JOIN attempts a
    ON aa.attempt_id = a.attempt_id

JOIN questions q
    ON aa.question_id = q.question_id

WHERE a.test_id <> q.test_id;


-- ============================================================
-- QA-DB-011: Validate attempt score against marks_obtained
-- Expected: 0 rows
-- ============================================================

SELECT
    a.attempt_id,
    s.student_name,
    t.test_name,
    a.score AS stored_score,
    COALESCE(SUM(aa.marks_obtained), 0) AS calculated_score

FROM attempts a

JOIN students s
    ON a.student_id = s.student_id

JOIN tests t
    ON a.test_id = t.test_id

LEFT JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id

GROUP BY
    a.attempt_id,
    s.student_name,
    t.test_name,
    a.score

HAVING a.score <> COALESCE(SUM(aa.marks_obtained), 0);


-- ============================================================
-- QA-DB-012: Validate test series configuration
-- Expected: 0 rows
-- ============================================================

SELECT
    series_id,
    series_name

FROM test_series

WHERE series_name NOT IN (
    'Part Test',
    'Customized Test',
    'Full Length Test'
);


-- ============================================================
-- QA-DB-013: Validate subject configuration
-- Expected: 0 rows
-- ============================================================

SELECT
    subject_id,
    subject_name

FROM subjects

WHERE subject_name NOT IN (
    'Biology',
    'Chemistry',
    'Physics'
);


-- ============================================================
-- QA-DB-014: Validate every test has a valid subject
-- Expected: 0 rows
-- ============================================================

SELECT
    t.test_id,
    t.subject_id

FROM tests t

LEFT JOIN subjects s
    ON t.subject_id = s.subject_id

WHERE s.subject_id IS NULL;


-- ============================================================
-- QA-DB-015: Validate every test has a valid test series
-- Expected: 0 rows
-- ============================================================

SELECT
    t.test_id,
    t.series_id

FROM tests t

LEFT JOIN test_series ts
    ON t.series_id = ts.series_id

WHERE ts.series_id IS NULL;
-- QA-DB-006-DIAGNOSTIC:
-- Identify all attempt score mismatches

SELECT
    a.attempt_id,
    s.student_name,
    t.test_name,

    a.score AS stored_score,

    SUM(
        CASE
            WHEN aa.is_correct = 1 THEN 1
            ELSE 0
        END
    ) AS correct_answers,

    SUM(
        CASE
            WHEN aa.is_correct = 0
                 AND aa.selected_answer IS NOT NULL
            THEN 1
            ELSE 0
        END
    ) AS wrong_answers,

    SUM(
        CASE
            WHEN aa.selected_answer IS NULL THEN 1
            ELSE 0
        END
    ) AS unattempted_answers,

    SUM(aa.marks_obtained) AS expected_score,

    a.score - SUM(aa.marks_obtained) AS score_difference

FROM attempts a

JOIN students s
    ON a.student_id = s.student_id

JOIN tests t
    ON a.test_id = t.test_id

JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id

GROUP BY
    a.attempt_id,
    s.student_name,
    t.test_name,
    a.score

HAVING a.score <> SUM(aa.marks_obtained)

ORDER BY a.attempt_id;

