PRAGMA foreign_keys = ON;

-- ============================================================
-- USERS
-- ============================================================

INSERT INTO users
    (name, email, password, role, is_active)
VALUES
    ('Aarav Sharma', 'aarav@example.com', 'Password123', 'student', 1),
    ('Priya Singh', 'priya@example.com', 'Password123', 'student', 1),
    ('Rahul Verma', 'rahul@example.com', 'Password123', 'student', 1),
    ('Neha Patel', 'neha@example.com', 'Password123', 'student', 1),
    ('Admin User', 'admin@example.com', 'Admin123', 'admin', 1);


-- ============================================================
-- SUBSCRIPTION PLANS
-- ============================================================

INSERT INTO plans
    (plan_name, price, duration_days, max_courses, is_active)
VALUES
    ('Free', 0.00, 30, 1, 1),
    ('Basic', 499.00, 30, 2, 1),
    ('Premium', 999.00, 90, 10, 1),
    ('Annual', 4999.00, 365, 10, 1);


-- ============================================================
-- COURSES
-- ============================================================

INSERT INTO courses
    (course_name, subject, is_active)
VALUES
    ('Python Fundamentals', 'Programming', 1),
    ('Advanced Python', 'Programming', 1),
    ('Physics Fundamentals', 'Physics', 1),
    ('Chemistry Fundamentals', 'Chemistry', 1),
    ('Biology Fundamentals', 'Biology', 1),
    ('Mathematics Fundamentals', 'Mathematics', 1);