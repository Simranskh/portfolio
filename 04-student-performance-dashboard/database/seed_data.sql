-- ============================================================
-- STUDENT PERFORMANCE DASHBOARD
-- FINAL SEED DATA
-- ============================================================
--
-- Subjects:
--   Biology
--   Chemistry
--   Physics
--
-- Test Series:
--   Part Test
--   Customized Test
--   Full Length Test
--
-- Every test:
--   180 questions
--   4 marks per question
--   720 total marks
--   360 pass marks
--
-- Scoring:
--   Correct     = +4
--   Wrong       = -1
--   Unattempted = 0
--
-- Total:
--   Students       = 5
--   Subjects       = 3
--   Test Series    = 3
--   Tests          = 9
--   Questions      = 1620
--   Attempts       = 25
--   Answers        = 4500
-- ============================================================


-- ============================================================
-- STUDENTS
-- ============================================================

INSERT INTO students
(student_name, email, registration_date)
VALUES
('Aarav Sharma', 'aarav@example.com', '2026-01-10'),
('Priya Singh', 'priya@example.com', '2026-01-12'),
('Rahul Verma', 'rahul@example.com', '2026-01-15'),
('Neha Patel', 'neha@example.com', '2026-01-18'),
('Vikram Joshi', 'vikram@example.com', '2026-01-20');


-- ============================================================
-- SUBJECTS
-- ============================================================

INSERT INTO subjects
(subject_name)
VALUES
('Biology'),
('Chemistry'),
('Physics');


-- ============================================================
-- TEST SERIES
-- ============================================================

INSERT INTO test_series
(series_name, description)
VALUES
('Part Test', 'Subject-wise practice test'),
('Customized Test', 'Customized test based on selected topics'),
('Full Length Test', 'Complete examination practice test');


-- ============================================================
-- TESTS
-- ============================================================

INSERT INTO tests
(series_id, subject_id, test_name, total_marks, pass_marks)
VALUES

-- Part Tests
(1, 1, 'Biology Part Test', 720, 360),
(1, 2, 'Chemistry Part Test', 720, 360),
(1, 3, 'Physics Part Test', 720, 360),

-- Customized Tests
(2, 1, 'Biology Customized Test', 720, 360),
(2, 2, 'Chemistry Customized Test', 720, 360),
(2, 3, 'Physics Customized Test', 720, 360),

-- Full Length Tests
(3, 1, 'Biology Full Length Test', 720, 360),
(3, 2, 'Chemistry Full Length Test', 720, 360),
(3, 3, 'Physics Full Length Test', 720, 360);


-- ============================================================
-- QUESTIONS
--
-- 180 questions per test
-- 9 tests × 180 = 1620 questions
-- Every question = 4 marks
-- ============================================================

WITH RECURSIVE question_numbers(question_no) AS (

    SELECT 1

    UNION ALL

    SELECT question_no + 1
    FROM question_numbers
    WHERE question_no < 180
)

INSERT INTO questions
(test_id, question_text, marks)

SELECT
    t.test_id,

    CASE t.test_id
        WHEN 1 THEN 'Biology Part Test - Question ' || q.question_no
        WHEN 2 THEN 'Chemistry Part Test - Question ' || q.question_no
        WHEN 3 THEN 'Physics Part Test - Question ' || q.question_no
        WHEN 4 THEN 'Biology Customized Test - Question ' || q.question_no
        WHEN 5 THEN 'Chemistry Customized Test - Question ' || q.question_no
        WHEN 6 THEN 'Physics Customized Test - Question ' || q.question_no
        WHEN 7 THEN 'Biology Full Length Test - Question ' || q.question_no
        WHEN 8 THEN 'Chemistry Full Length Test - Question ' || q.question_no
        WHEN 9 THEN 'Physics Full Length Test - Question ' || q.question_no
    END AS question_text,

    4 AS marks

FROM tests t

CROSS JOIN question_numbers q

ORDER BY
    t.test_id,
    q.question_no;


-- ============================================================
-- ATTEMPTS
--
-- Score formula:
--
--     (correct × 4) - wrong
--
-- Unattempted = 0
-- Total questions = 180
-- Total marks = 720
-- ============================================================

INSERT INTO attempts
(student_id, test_id, attempted_at, score, total_marks, status)
VALUES

-- ============================================================
-- AARAV SHARMA
-- ============================================================

(1, 1, '2026-02-01 10:00:00', 500, 720, 'passed'),
(1, 2, '2026-02-03 11:00:00', 450, 720, 'passed'),
(1, 3, '2026-02-05 14:00:00', 320, 720, 'failed'),
(1, 4, '2026-02-08 10:00:00', 545, 720, 'passed'),
(1, 7, '2026-02-15 09:00:00', 590, 720, 'passed'),


-- ============================================================
-- PRIYA SINGH
-- ============================================================

(2, 1, '2026-02-01 10:30:00', 475, 720, 'passed'),
(2, 2, '2026-02-03 11:30:00', 560, 720, 'passed'),
(2, 3, '2026-02-05 14:30:00', 520, 720, 'passed'),
(2, 5, '2026-02-09 10:30:00', 520, 720, 'passed'),
(2, 8, '2026-02-16 09:30:00', 600, 720, 'passed'),


-- ============================================================
-- RAHUL VERMA
-- ============================================================

(3, 1, '2026-02-02 09:00:00', 380, 720, 'passed'),
(3, 2, '2026-02-04 10:00:00', 300, 720, 'failed'),
(3, 3, '2026-02-06 15:00:00', 410, 720, 'passed'),
(3, 6, '2026-02-10 11:00:00', 350, 720, 'failed'),
(3, 9, '2026-02-17 10:00:00', 290, 720, 'failed'),


-- ============================================================
-- NEHA PATEL
-- ============================================================

(4, 1, '2026-02-02 09:30:00', 610, 720, 'passed'),
(4, 2, '2026-02-04 10:30:00', 570, 720, 'passed'),
(4, 3, '2026-02-06 15:30:00', 588, 720, 'passed'),
(4, 6, '2026-02-10 11:30:00', 600, 720, 'passed'),
(4, 9, '2026-02-17 10:30:00', 650, 720, 'passed'),


-- ============================================================
-- VIKRAM JOSHI
-- ============================================================

(5, 1, '2026-02-02 10:00:00', 280, 720, 'failed'),
(5, 2, '2026-02-04 11:00:00', 390, 720, 'passed'),
(5, 3, '2026-02-06 16:00:00', 250, 720, 'failed'),
(5, 5, '2026-02-11 12:00:00', 330, 720, 'failed'),
(5, 8, '2026-02-18 11:00:00', 480, 720, 'passed');


-- ============================================================
-- ATTEMPT ANSWERS
--
-- Every attempt = 180 answers
--
-- Correct:
--   is_correct = 1
--   selected_answer = 'Option A'
--   marks_obtained = 4
--
-- Wrong:
--   is_correct = 0
--   selected_answer = 'Option B'
--   marks_obtained = -1
--
-- Unattempted:
--   is_correct = 0
--   selected_answer = NULL
--   marks_obtained = 0
--
-- Score:
--   (correct × 4) - wrong
-- ============================================================

WITH RECURSIVE question_numbers(question_no) AS (

    SELECT 1

    UNION ALL

    SELECT question_no + 1
    FROM question_numbers
    WHERE question_no < 180
),

attempt_plan(
    attempt_id,
    student_id,
    test_id,
    correct_count,
    wrong_count
) AS (

    -- ========================================================
    -- AARAV SHARMA
    -- ========================================================

    SELECT 1, 1, 1, 130, 20
    UNION ALL SELECT 2, 1, 2, 120, 30
    UNION ALL SELECT 3, 1, 3, 90, 40
    UNION ALL SELECT 4, 1, 4, 140, 15
    UNION ALL SELECT 5, 1, 7, 150, 10


    -- ========================================================
    -- PRIYA SINGH
    -- ========================================================

    UNION ALL SELECT 6, 2, 1, 125, 25
    UNION ALL SELECT 7, 2, 2, 145, 20
    UNION ALL SELECT 8, 2, 3, 135, 20
    UNION ALL SELECT 9, 2, 5, 135, 20
    UNION ALL SELECT 10, 2, 8, 150, 0


    -- ========================================================
    -- RAHUL VERMA
    -- ========================================================

    UNION ALL SELECT 11, 3, 1, 100, 20
    UNION ALL SELECT 12, 3, 2, 80, 20
    UNION ALL SELECT 13, 3, 3, 110, 30
    UNION ALL SELECT 14, 3, 6, 90, 10
    UNION ALL SELECT 15, 3, 9, 80, 30


    -- ========================================================
    -- NEHA PATEL
    -- ========================================================

    UNION ALL SELECT 16, 4, 1, 155, 10
    UNION ALL SELECT 17, 4, 2, 145, 10
    UNION ALL SELECT 18, 4, 3, 150, 12
    UNION ALL SELECT 19, 4, 6, 155, 20
    UNION ALL SELECT 20, 4, 9, 165, 10


    -- ========================================================
    -- VIKRAM JOSHI
    -- ========================================================

    UNION ALL SELECT 21, 5, 1, 75, 20
    UNION ALL SELECT 22, 5, 2, 100, 10
    UNION ALL SELECT 23, 5, 3, 65, 10
    UNION ALL SELECT 24, 5, 5, 85, 10
    UNION ALL SELECT 25, 5, 8, 120, 0
)

INSERT INTO attempt_answers
(
    attempt_id,
    question_id,
    selected_answer,
    is_correct,
    marks_obtained
)

SELECT

    ap.attempt_id,

    q.question_id,

    CASE
        WHEN qn.question_no <= ap.correct_count
            THEN 'Option A'

        WHEN qn.question_no <=
             ap.correct_count + ap.wrong_count
            THEN 'Option B'

        ELSE NULL
    END AS selected_answer,

    CASE
        WHEN qn.question_no <= ap.correct_count
            THEN 1
        ELSE 0
    END AS is_correct,

    CASE
        WHEN qn.question_no <= ap.correct_count
            THEN 4

        WHEN qn.question_no <=
             ap.correct_count + ap.wrong_count
            THEN -1

        ELSE 0
    END AS marks_obtained

FROM attempt_plan ap

JOIN questions q
    ON q.test_id = ap.test_id

JOIN question_numbers qn
    ON qn.question_no =
       CAST(
           SUBSTR(
               q.question_text,
               INSTR(q.question_text, 'Question ') + 9
           ) AS INTEGER
       )

ORDER BY
    ap.attempt_id,
    qn.question_no;