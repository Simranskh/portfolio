PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS entitlements;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS plans;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'student',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK(price >= 0),
    duration_days INTEGER NOT NULL CHECK(duration_days > 0),
    max_courses INTEGER NOT NULL CHECK(max_courses > 0),
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT NOT NULL
        CHECK(status IN ('active', 'expired', 'cancelled')),
    auto_renew INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK(amount >= 0),
    payment_method TEXT NOT NULL,
    transaction_id TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL
        CHECK(status IN ('pending', 'success', 'failed', 'refunded')),
    paid_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL UNIQUE,
    subject TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE entitlements (
    entitlement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    granted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    revoked_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id),
    UNIQUE(user_id, course_id, subscription_id)
);

CREATE TABLE audit_logs (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    details TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_users_email
ON users(email);

CREATE INDEX idx_subscriptions_user
ON subscriptions(user_id);

CREATE INDEX idx_subscriptions_status
ON subscriptions(status);

CREATE INDEX idx_payments_user
ON payments(user_id);

CREATE INDEX idx_entitlements_user
ON entitlements(user_id);

CREATE INDEX idx_entitlements_course
ON entitlements(course_id);