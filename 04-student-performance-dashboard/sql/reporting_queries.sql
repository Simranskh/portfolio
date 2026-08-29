-- ============================================================
-- REPORTING QUERIES
-- Student Performance Dashboard
-- SQLite Compatible
-- ============================================================


-- ============================================================
-- QA-REPORT-001: Student Performance Summary
-- ============================================================

SELECT
    s.student_id,
    s.student_name,

    COUNT(a.attempt_id) AS total_attempts,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    MIN(a.score) AS lowest_score

FROM students s

LEFT JOIN attempts a
    ON s.student_id = a.student_id

GROUP BY
    s.student_id,
    s.student_name

ORDER BY
    average_score DESC;


-- ============================================================
-- QA-REPORT-002: Subject-wise Performance
-- ============================================================

SELECT
    sub.subject_id,
    sub.subject_name,

    COUNT(a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    MIN(a.score) AS lowest_score,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts

FROM subjects sub

LEFT JOIN tests t
    ON sub.subject_id = t.subject_id

LEFT JOIN attempts a
    ON t.test_id = a.test_id

GROUP BY
    sub.subject_id,
    sub.subject_name

ORDER BY
    average_score DESC;


-- ============================================================
-- QA-REPORT-003: Test Series Performance
-- ============================================================

SELECT
    ts.series_id,
    ts.series_name,

    COUNT(a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    MIN(a.score) AS lowest_score,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts

FROM test_series ts

LEFT JOIN tests t
    ON ts.series_id = t.series_id

LEFT JOIN attempts a
    ON t.test_id = a.test_id

GROUP BY
    ts.series_id,
    ts.series_name

ORDER BY
    average_score DESC;


-- ============================================================
-- QA-REPORT-004: Student Ranking
-- ============================================================

SELECT
    RANK() OVER (
        ORDER BY AVG(a.score) DESC
    ) AS student_rank,

    s.student_id,
    s.student_name,

    COUNT(a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts

FROM students s

JOIN attempts a
    ON s.student_id = a.student_id

GROUP BY
    s.student_id,
    s.student_name

ORDER BY
    student_rank;


-- ============================================================
-- QA-REPORT-005: Answer Performance Analysis
-- ============================================================

SELECT
    s.student_name,
    t.test_name,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted_answers,

    SUM(aa.marks_obtained) AS final_score

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
    t.test_name

ORDER BY
    s.student_name,
    a.attempt_id;


-- ============================================================
-- QA-REPORT-006: Student Pass Percentage
-- ============================================================

SELECT
    s.student_id,
    s.student_name,

    COUNT(a.attempt_id) AS total_attempts,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts,

    ROUND(
        100.0 *
        COUNT(
            CASE
                WHEN a.status = 'passed' THEN a.attempt_id
            END
        )
        /
        NULLIF(COUNT(a.attempt_id), 0),
        2
    ) AS pass_percentage

FROM students s

JOIN attempts a
    ON s.student_id = a.student_id

GROUP BY
    s.student_id,
    s.student_name

ORDER BY
    pass_percentage DESC;


-- ============================================================
-- QA-REPORT-007: Student-wise Subject Performance
-- ============================================================

SELECT
    s.student_id,
    s.student_name,

    sub.subject_id,
    sub.subject_name,

    COUNT(a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    MIN(a.score) AS lowest_score,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts

FROM students s

JOIN attempts a
    ON s.student_id = a.student_id

JOIN tests t
    ON a.test_id = t.test_id

JOIN subjects sub
    ON t.subject_id = sub.subject_id

GROUP BY
    s.student_id,
    s.student_name,
    sub.subject_id,
    sub.subject_name

ORDER BY
    s.student_id,
    average_score DESC;


-- ============================================================
-- QA-REPORT-008: Strongest and Weakest Subject per Student
-- ============================================================

WITH subject_performance AS (

    SELECT
        s.student_id,
        s.student_name,
        sub.subject_id,
        sub.subject_name,

        ROUND(AVG(a.score), 2) AS average_score

    FROM students s

    JOIN attempts a
        ON s.student_id = a.student_id

    JOIN tests t
        ON a.test_id = t.test_id

    JOIN subjects sub
        ON t.subject_id = sub.subject_id

    GROUP BY
        s.student_id,
        s.student_name,
        sub.subject_id,
        sub.subject_name
),

ranked_subjects AS (

    SELECT
        student_id,
        student_name,
        subject_name,
        average_score,

        RANK() OVER (
            PARTITION BY student_id
            ORDER BY average_score DESC
        ) AS strongest_rank,

        RANK() OVER (
            PARTITION BY student_id
            ORDER BY average_score ASC
        ) AS weakest_rank

    FROM subject_performance
)

SELECT
    student_id,
    student_name,

    MAX(
        CASE
            WHEN strongest_rank = 1
            THEN subject_name
        END
    ) AS strongest_subject,

    MAX(
        CASE
            WHEN strongest_rank = 1
            THEN average_score
        END
    ) AS strongest_average_score,

    MAX(
        CASE
            WHEN weakest_rank = 1
            THEN subject_name
        END
    ) AS weakest_subject,

    MAX(
        CASE
            WHEN weakest_rank = 1
            THEN average_score
        END
    ) AS weakest_average_score

FROM ranked_subjects

GROUP BY
    student_id,
    student_name

ORDER BY
    student_id;


-- ============================================================
-- QA-REPORT-009: Test-wise Performance
-- ============================================================

SELECT
    t.test_id,
    t.test_name,

    sub.subject_name,

    ts.series_name,

    COUNT(a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    MIN(a.score) AS lowest_score,

    COUNT(
        CASE
            WHEN a.status = 'passed' THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        CASE
            WHEN a.status = 'failed' THEN a.attempt_id
        END
    ) AS failed_attempts

FROM tests t

JOIN subjects sub
    ON t.subject_id = sub.subject_id

JOIN test_series ts
    ON t.series_id = ts.series_id

LEFT JOIN attempts a
    ON t.test_id = a.test_id

GROUP BY
    t.test_id,
    t.test_name,
    sub.subject_name,
    ts.series_name

ORDER BY
    average_score DESC;


-- ============================================================
-- QA-REPORT-010: Overall Dashboard KPIs
-- ============================================================

SELECT

    (
        SELECT COUNT(*)
        FROM students
    ) AS total_students,

    (
        SELECT COUNT(*)
        FROM subjects
    ) AS total_subjects,

    (
        SELECT COUNT(*)
        FROM test_series
    ) AS total_test_series,

    (
        SELECT COUNT(*)
        FROM tests
    ) AS total_tests,

    (
        SELECT COUNT(*)
        FROM questions
    ) AS total_questions,

    (
        SELECT COUNT(*)
        FROM attempts
    ) AS total_attempts,

    (
        SELECT COUNT(*)
        FROM attempt_answers
    ) AS total_attempt_answers,

    (
        SELECT COUNT(*)
        FROM attempts
        WHERE status = 'passed'
    ) AS total_passed_attempts,

    (
        SELECT COUNT(*)
        FROM attempts
        WHERE status = 'failed'
    ) AS total_failed_attempts,

    (
        SELECT ROUND(AVG(score), 2)
        FROM attempts
    ) AS overall_average_score,

    (
        SELECT MAX(score)
        FROM attempts
    ) AS highest_score,

    (
        SELECT MIN(score)
        FROM attempts
    ) AS lowest_score,

    (
        SELECT
            ROUND(
                100.0 *
                COUNT(
                    CASE
                        WHEN status = 'passed'
                        THEN attempt_id
                    END
                )
                /
                NULLIF(COUNT(*), 0),
                2
            )
        FROM attempts
    ) AS overall_pass_percentage;


-- ============================================================
-- QA-REPORT-011: Student Detailed Performance
-- ============================================================

SELECT
    s.student_id,
    s.student_name,

    COUNT(DISTINCT a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    MAX(a.score) AS highest_score,

    MIN(a.score) AS lowest_score,

    COUNT(
        DISTINCT CASE
            WHEN a.status = 'passed'
            THEN a.attempt_id
        END
    ) AS passed_attempts,

    COUNT(
        DISTINCT CASE
            WHEN a.status = 'failed'
            THEN a.attempt_id
        END
    ) AS failed_attempts,

    ROUND(
        100.0 *
        COUNT(
            DISTINCT CASE
                WHEN a.status = 'passed'
                THEN a.attempt_id
            END
        )
        /
        NULLIF(COUNT(DISTINCT a.attempt_id), 0),
        2
    ) AS pass_percentage,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS total_correct_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS total_wrong_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS total_unattempted_questions

FROM students s

JOIN attempts a
    ON s.student_id = a.student_id

JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id

GROUP BY
    s.student_id,
    s.student_name

ORDER BY
    average_score DESC;


-- ============================================================
-- QA-REPORT-012: Attempt-Level Detailed Performance
-- ============================================================

SELECT
    a.attempt_id,

    s.student_name,

    sub.subject_name,

    ts.series_name,

    t.test_name,

    a.attempted_at,

    a.score,

    a.total_marks,

    a.status,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted_answers,

    ROUND(
        100.0 * a.score / NULLIF(a.total_marks, 0),
        2
    ) AS score_percentage

FROM attempts a

JOIN students s
    ON a.student_id = s.student_id

JOIN tests t
    ON a.test_id = t.test_id

JOIN subjects sub
    ON t.subject_id = sub.subject_id

JOIN test_series ts
    ON t.series_id = ts.series_id

JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id

GROUP BY
    a.attempt_id,
    s.student_name,
    sub.subject_name,
    ts.series_name,
    t.test_name,
    a.attempted_at,
    a.score,
    a.total_marks,
    a.status

ORDER BY
    a.attempt_id;


-- ============================================================
-- QA-REPORT-013: Score Distribution
-- ============================================================

SELECT
    CASE
        WHEN score * 100.0 / NULLIF(total_marks, 0) >= 80
            THEN 'Excellent'

        WHEN score * 100.0 / NULLIF(total_marks, 0) >= 60
            THEN 'Good'

        WHEN score * 100.0 / NULLIF(total_marks, 0) >= 40
            THEN 'Average'

        ELSE 'Poor'
    END AS performance_band,

    COUNT(*) AS attempt_count,

    ROUND(
        100.0 * COUNT(*) /
        NULLIF((SELECT COUNT(*) FROM attempts), 0),
        2
    ) AS percentage_of_attempts

FROM attempts

GROUP BY
    CASE
        WHEN score * 100.0 / NULLIF(total_marks, 0) >= 80
            THEN 'Excellent'

        WHEN score * 100.0 / NULLIF(total_marks, 0) >= 60
            THEN 'Good'

        WHEN score * 100.0 / NULLIF(total_marks, 0) >= 40
            THEN 'Average'

        ELSE 'Poor'
    END

ORDER BY
    CASE performance_band
        WHEN 'Excellent' THEN 1
        WHEN 'Good' THEN 2
        WHEN 'Average' THEN 3
        ELSE 4
    END;


-- ============================================================
-- QA-REPORT-014: Student Performance Trend
-- ============================================================

WITH attempt_trend AS (

    SELECT
        a.attempt_id,
        s.student_id,
        s.student_name,
        a.attempted_at,
        a.score,

        LAG(a.score) OVER (
            PARTITION BY s.student_id
            ORDER BY a.attempted_at, a.attempt_id
        ) AS previous_score

    FROM attempts a

    JOIN students s
        ON a.student_id = s.student_id
)

SELECT
    student_id,
    student_name,
    attempt_id,
    attempted_at,
    score,
    previous_score,

    CASE
        WHEN previous_score IS NULL
            THEN 'First Attempt'

        WHEN score > previous_score
            THEN 'Improved'

        WHEN score < previous_score
            THEN 'Declined'

        ELSE 'No Change'
    END AS performance_trend,

    CASE
        WHEN previous_score IS NULL
            THEN NULL
        ELSE score - previous_score
    END AS score_change

FROM attempt_trend

ORDER BY
    student_id,
    attempted_at,
    attempt_id;


-- ============================================================
-- QA-REPORT-015: Subject-wise Answer Accuracy
-- ============================================================

SELECT
    sub.subject_id,
    sub.subject_name,

    COUNT(aa.answer_id) AS total_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong_answers,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted_answers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS accuracy_percentage,

    ROUND(
        AVG(a.score),
        2
    ) AS average_attempt_score

FROM subjects sub

JOIN tests t
    ON sub.subject_id = t.subject_id

JOIN attempts a
    ON t.test_id = a.test_id

JOIN attempt_answers aa
    ON a.attempt_id = aa.attempt_id

GROUP BY
    sub.subject_id,
    sub.subject_name

ORDER BY
    accuracy_percentage DESC;


-- ============================================================
-- QA-REPORT-016: Top 5 Individual Performances
-- ============================================================

SELECT
    ROW_NUMBER() OVER (
        ORDER BY a.score DESC, a.attempt_id
    ) AS performance_rank,

    s.student_name,

    sub.subject_name,

    t.test_name,

    a.score,

    a.total_marks,

    ROUND(
        100.0 * a.score / NULLIF(a.total_marks, 0),
        2
    ) AS score_percentage,

    a.status,

    a.attempted_at

FROM attempts a

JOIN students s
    ON a.student_id = s.student_id

JOIN tests t
    ON a.test_id = t.test_id

JOIN subjects sub
    ON t.subject_id = sub.subject_id

ORDER BY
    a.score DESC,
    a.attempt_id

LIMIT 5;


-- ============================================================
-- QA-REPORT-017: Most Difficult Tests
-- ============================================================

SELECT
    t.test_id,
    t.test_name,

    sub.subject_name,

    ts.series_name,

    COUNT(a.attempt_id) AS total_attempts,

    ROUND(AVG(a.score), 2) AS average_score,

    ROUND(
        100.0 *
        COUNT(
            CASE
                WHEN a.status = 'passed'
                THEN a.attempt_id
            END
        )
        /
        NULLIF(COUNT(a.attempt_id), 0),
        2
    ) AS pass_percentage,

    MIN(a.score) AS lowest_score,

    MAX(a.score) AS highest_score

FROM tests t

JOIN subjects sub
    ON t.subject_id = sub.subject_id

JOIN test_series ts
    ON t.series_id = ts.series_id

JOIN attempts a
    ON t.test_id = a.test_id

GROUP BY
    t.test_id,
    t.test_name,
    sub.subject_name,
    ts.series_name

ORDER BY
    average_score ASC,
    pass_percentage ASC;


-- ============================================================
-- QA-REPORT-018: Question-Level Difficulty
-- ============================================================
-- Accuracy = Correct / Attempted × 100
-- Unattempted answers are excluded.
-- Questions with zero attempted responses are excluded.
-- ============================================================

WITH question_performance AS (

    SELECT
        q.question_id,
        q.test_id,
        t.test_name,
        s.subject_name,
        q.marks,

        COUNT(aa.answer_id) AS total_responses,

        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                THEN 1
                ELSE 0
            END
        ) AS attempted,

        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        ) AS correct,

        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 0
                THEN 1
                ELSE 0
            END
        ) AS wrong,

        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
                THEN 1
                ELSE 0
            END
        ) AS unattempted

    FROM questions q

    JOIN tests t
        ON q.test_id = t.test_id

    JOIN subjects s
        ON t.subject_id = s.subject_id

    JOIN attempt_answers aa
        ON aa.question_id = q.question_id

    GROUP BY
        q.question_id,
        q.test_id,
        t.test_name,
        s.subject_name,
        q.marks
)

SELECT
    question_id,
    test_id,
    test_name,
    subject_name,
    marks,

    total_responses,
    attempted,
    correct,
    wrong,
    unattempted,

    ROUND(
        100.0 * correct / NULLIF(attempted, 0),
        2
    ) AS accuracy_percentage

FROM question_performance

WHERE attempted > 0

ORDER BY
    accuracy_percentage ASC,
    wrong DESC,
    question_id ASC;


-- ============================================================
-- QA-REPORT-019: Test-Level Performance Summary
-- ============================================================

SELECT
    t.test_id,
    t.test_name,
    s.subject_name,

    COUNT(DISTINCT q.question_id) AS total_questions,

    COUNT(aa.answer_id) AS total_responses,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
            THEN 1
            ELSE 0
        END
    ) AS attempted,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS accuracy_percentage

FROM tests t

JOIN subjects s
    ON t.subject_id = s.subject_id

JOIN questions q
    ON q.test_id = t.test_id

LEFT JOIN attempt_answers aa
    ON aa.question_id = q.question_id

GROUP BY
    t.test_id,
    t.test_name,
    s.subject_name

ORDER BY
    accuracy_percentage ASC,
    t.test_id;


-- ============================================================
-- QA-REPORT-020: Subject-Level Performance Summary
-- ============================================================

SELECT
    s.subject_id,
    s.subject_name,

    COUNT(DISTINCT t.test_id) AS total_tests,

    COUNT(DISTINCT q.question_id) AS total_questions,

    COUNT(aa.answer_id) AS total_responses,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
            THEN 1
            ELSE 0
        END
    ) AS attempted,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS accuracy_percentage

FROM subjects s

JOIN tests t
    ON t.subject_id = s.subject_id

JOIN questions q
    ON q.test_id = t.test_id

LEFT JOIN attempt_answers aa
    ON aa.question_id = q.question_id

GROUP BY
    s.subject_id,
    s.subject_name

ORDER BY
    accuracy_percentage ASC,
    s.subject_id;


-- ============================================================
-- QA-REPORT-021: Student-Level Performance Summary
-- ============================================================

SELECT
    a.student_id,

    COUNT(DISTINCT a.test_id) AS total_tests_attempted,

    COUNT(DISTINCT aa.question_id) AS total_questions,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
            THEN 1
            ELSE 0
        END
    ) AS attempted,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS accuracy_percentage

FROM attempts a

JOIN attempt_answers aa
    ON aa.attempt_id = a.attempt_id

GROUP BY
    a.student_id

ORDER BY
    accuracy_percentage ASC,
    a.student_id;


-- ============================================================
-- QA-REPORT-022: Student × Subject Performance
-- ============================================================

SELECT
    a.student_id,

    s.subject_id,
    s.subject_name,

    COUNT(DISTINCT a.test_id) AS total_tests_attempted,

    COUNT(DISTINCT aa.question_id) AS total_questions,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
            THEN 1
            ELSE 0
        END
    ) AS attempted,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 1
            THEN 1
            ELSE 0
        END
    ) AS correct,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                 AND aa.is_correct = 0
            THEN 1
            ELSE 0
        END
    ) AS wrong,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS accuracy_percentage

FROM attempts a

JOIN attempt_answers aa
    ON aa.attempt_id = a.attempt_id

JOIN tests t
    ON a.test_id = t.test_id

JOIN subjects s
    ON t.subject_id = s.subject_id

GROUP BY
    a.student_id,
    s.subject_id,
    s.subject_name

ORDER BY
    a.student_id,
    accuracy_percentage ASC,
    s.subject_id;


-- ============================================================
-- QA-REPORT-023: Test Completion / Attempt Rate
-- ============================================================
-- Total students = all students in students table.
-- ============================================================

SELECT
    t.test_id,
    t.test_name,
    s.subject_name,

    COUNT(DISTINCT a.student_id) AS students_attempted,

    (
        SELECT COUNT(*)
        FROM students
    ) AS total_students,

    ROUND(
        100.0 *
        COUNT(DISTINCT a.student_id)
        /
        NULLIF(
            (
                SELECT COUNT(*)
                FROM students
            ),
            0
        ),
        2
    ) AS completion_rate_percentage

FROM tests t

JOIN subjects s
    ON t.subject_id = s.subject_id

LEFT JOIN attempts a
    ON a.test_id = t.test_id

GROUP BY
    t.test_id,
    t.test_name,
    s.subject_name

ORDER BY
    completion_rate_percentage ASC,
    t.test_id;


-- ============================================================
-- QA-REPORT-024: Question Attempt & Unattempted Analysis
-- ============================================================

SELECT
    q.question_id,
    q.test_id,
    t.test_name,
    s.subject_name,

    COUNT(aa.answer_id) AS total_responses,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
            THEN 1
            ELSE 0
        END
    ) AS attempted,

    SUM(
        CASE
            WHEN TRIM(COALESCE(aa.selected_answer, '')) = ''
            THEN 1
            ELSE 0
        END
    ) AS unattempted,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(COUNT(aa.answer_id), 0),
        2
    ) AS attempt_rate_percentage

FROM questions q

JOIN tests t
    ON q.test_id = t.test_id

JOIN subjects s
    ON t.subject_id = s.subject_id

LEFT JOIN attempt_answers aa
    ON aa.question_id = q.question_id

GROUP BY
    q.question_id,
    q.test_id,
    t.test_name,
    s.subject_name

HAVING
    COUNT(aa.answer_id) > 0

ORDER BY
    attempt_rate_percentage ASC,
    q.question_id;


-- ============================================================
-- QA-REPORT-025: Question Difficulty Classification
-- ============================================================
-- Accuracy:
-- 0–30       = Very Hard
-- >30–50     = Hard
-- >50–70     = Moderate
-- >70–85     = Easy
-- >85–100    = Very Easy
--
-- Accuracy is based ONLY on attempted responses.
-- ============================================================

WITH question_accuracy AS (

    SELECT
        q.question_id,
        q.test_id,
        t.test_name,
        s.subject_name,

        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        ) AS correct,

        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                THEN 1
                ELSE 0
            END
        ) AS attempted

    FROM questions q

    JOIN tests t
        ON q.test_id = t.test_id

    JOIN subjects s
        ON t.subject_id = s.subject_id

    JOIN attempt_answers aa
        ON aa.question_id = q.question_id

    GROUP BY
        q.question_id,
        q.test_id,
        t.test_name,
        s.subject_name
)

SELECT
    question_id,
    test_id,
    test_name,
    subject_name,

    attempted,
    correct,

    ROUND(
        100.0 * correct / NULLIF(attempted, 0),
        2
    ) AS accuracy_percentage,

    CASE
        WHEN 100.0 * correct / NULLIF(attempted, 0) <= 30
            THEN 'Very Hard'

        WHEN 100.0 * correct / NULLIF(attempted, 0) <= 50
            THEN 'Hard'

        WHEN 100.0 * correct / NULLIF(attempted, 0) <= 70
            THEN 'Moderate'

        WHEN 100.0 * correct / NULLIF(attempted, 0) <= 85
            THEN 'Easy'

        ELSE 'Very Easy'
    END AS difficulty

FROM question_accuracy

WHERE attempted > 0

ORDER BY
    accuracy_percentage ASC,
    question_id;


-- ============================================================
-- QA-REPORT-026: Subject-wise Difficulty Distribution
-- ============================================================

WITH question_accuracy AS (

    SELECT
        q.question_id,
        s.subject_name,

        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ) AS accuracy

    FROM questions q

    JOIN tests t
        ON q.test_id = t.test_id

    JOIN subjects s
        ON t.subject_id = s.subject_id

    JOIN attempt_answers aa
        ON aa.question_id = q.question_id

    GROUP BY
        q.question_id,
        s.subject_name
),

classified AS (

    SELECT
        question_id,
        subject_name,

        CASE
            WHEN accuracy <= 30
                THEN 'Very Hard'

            WHEN accuracy <= 50
                THEN 'Hard'

            WHEN accuracy <= 70
                THEN 'Moderate'

            WHEN accuracy <= 85
                THEN 'Easy'

            ELSE 'Very Easy'
        END AS difficulty

    FROM question_accuracy
)

SELECT
    subject_name,
    difficulty,
    COUNT(*) AS question_count

FROM classified

GROUP BY
    subject_name,
    difficulty

ORDER BY
    subject_name,
    CASE difficulty
        WHEN 'Very Hard' THEN 1
        WHEN 'Hard' THEN 2
        WHEN 'Moderate' THEN 3
        WHEN 'Easy' THEN 4
        WHEN 'Very Easy' THEN 5
    END;


-- ============================================================
-- QA-REPORT-027: Overall Difficulty Distribution
-- ============================================================

WITH question_accuracy AS (

    SELECT
        q.question_id,

        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ) AS accuracy

    FROM questions q

    JOIN attempt_answers aa
        ON aa.question_id = q.question_id

    GROUP BY
        q.question_id
),

classified AS (

    SELECT
        question_id,

        CASE
            WHEN accuracy <= 30
                THEN 'Very Hard'

            WHEN accuracy <= 50
                THEN 'Hard'

            WHEN accuracy <= 70
                THEN 'Moderate'

            WHEN accuracy <= 85
                THEN 'Easy'

            ELSE 'Very Easy'
        END AS difficulty

    FROM question_accuracy

    WHERE accuracy IS NOT NULL
)

SELECT
    difficulty,
    COUNT(*) AS question_count

FROM classified

GROUP BY
    difficulty

ORDER BY
    CASE difficulty
        WHEN 'Very Hard' THEN 1
        WHEN 'Hard' THEN 2
        WHEN 'Moderate' THEN 3
        WHEN 'Easy' THEN 4
        WHEN 'Very Easy' THEN 5
    END;


-- ============================================================
-- QA-REPORT-028: Overall Difficulty Percentage
-- ============================================================

WITH question_accuracy AS (

    SELECT
        q.question_id,

        100.0 *
        SUM(
            CASE
                WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                     AND aa.is_correct = 1
                THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN TRIM(COALESCE(aa.selected_answer, '')) <> ''
                    THEN 1
                    ELSE 0
                END
            ),
            0
        ) AS accuracy

    FROM questions q

    JOIN attempt_answers aa
        ON aa.question_id = q.question_id

    GROUP BY
        q.question_id
),

classified AS (

    SELECT
        question_id,

        CASE
            WHEN accuracy <= 30
                THEN 'Very Hard'

            WHEN accuracy <= 50
                THEN 'Hard'

            WHEN accuracy <= 70
                THEN 'Moderate'

            WHEN accuracy <= 85
                THEN 'Easy'

            ELSE 'Very Easy'
        END AS difficulty

    FROM question_accuracy

    WHERE accuracy IS NOT NULL
)

SELECT
    difficulty,

    COUNT(*) AS question_count,

    ROUND(
        100.0 *
        COUNT(*)
        /
        NULLIF(
            (SELECT COUNT(*) FROM classified),
            0
        ),
        2
    ) AS percentage

FROM classified

GROUP BY
    difficulty

ORDER BY
    CASE difficulty
        WHEN 'Very Hard' THEN 1
        WHEN 'Hard' THEN 2
        WHEN 'Moderate' THEN 3
        WHEN 'Easy' THEN 4
        WHEN 'Very Easy' THEN 5
    END;


-- ============================================================
-- QA-REPORT-029: Subject-wise Overall Accuracy
-- ============================================================

SELECT
    s.subject_name,

    COUNT(*) AS attempted_answers,

    SUM(
        CASE
            WHEN aa.is_correct = 1 THEN 1
            ELSE 0
        END
    ) AS correct_answers,

    SUM(
        CASE
            WHEN aa.is_correct = 0 THEN 1
            ELSE 0
        END
    ) AS incorrect_answers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN aa.is_correct = 1 THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(COUNT(*), 0),
        2
    ) AS accuracy_percentage

FROM questions q

JOIN tests t
    ON q.test_id = t.test_id

JOIN subjects s
    ON t.subject_id = s.subject_id

JOIN attempt_answers aa
    ON aa.question_id = q.question_id

WHERE
    TRIM(COALESCE(aa.selected_answer, '')) <> ''

GROUP BY
    s.subject_name

ORDER BY
    s.subject_name;


-- ============================================================
-- QA-REPORT-030: Overall Accuracy
-- ============================================================

SELECT
    COUNT(*) AS attempted_answers,

    SUM(
        CASE
            WHEN aa.is_correct = 1 THEN 1
            ELSE 0
        END
    ) AS correct_answers,

    SUM(
        CASE
            WHEN aa.is_correct = 0 THEN 1
            ELSE 0
        END
    ) AS incorrect_answers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN aa.is_correct = 1 THEN 1
                ELSE 0
            END
        )
        /
        NULLIF(COUNT(*), 0),
        2
    ) AS accuracy_percentage

FROM questions q

JOIN attempt_answers aa
    ON aa.question_id = q.question_id

WHERE
    TRIM(COALESCE(aa.selected_answer, '')) <> '';