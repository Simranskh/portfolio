-- 1. Orphan subscriptions
SELECT s.subscription_id
FROM subscriptions s
LEFT JOIN users u
    ON s.user_id = u.user_id
WHERE u.user_id IS NULL;


-- 2. Invalid plan references
SELECT s.subscription_id
FROM subscriptions s
LEFT JOIN plans p
    ON s.plan_id = p.plan_id
WHERE p.plan_id IS NULL;


-- 3. Orphan payments
SELECT p.payment_id
FROM payments p
LEFT JOIN subscriptions s
    ON p.subscription_id = s.subscription_id
WHERE s.subscription_id IS NULL;


-- 4. Payment user mismatch
SELECT p.payment_id
FROM payments p
JOIN subscriptions s
    ON p.subscription_id = s.subscription_id
WHERE p.user_id != s.user_id;


-- 5. Negative plan price
SELECT plan_id
FROM plans
WHERE price < 0;


-- 6. Invalid plan duration
SELECT plan_id
FROM plans
WHERE duration_days <= 0;


-- 7. Invalid maximum courses
SELECT plan_id
FROM plans
WHERE max_courses <= 0;


-- 8. Invalid subscription status
SELECT subscription_id
FROM subscriptions
WHERE status NOT IN (
    'active',
    'expired',
    'cancelled'
);


-- 9. Active subscription already expired
SELECT subscription_id
FROM subscriptions
WHERE status = 'active'
AND datetime(end_date) < datetime('now');


-- 10. Expired subscription with future end date
SELECT subscription_id
FROM subscriptions
WHERE status = 'expired'
AND datetime(end_date) >= datetime('now');


-- 11. Cancelled subscription with auto-renew
SELECT subscription_id
FROM subscriptions
WHERE status = 'cancelled'
AND auto_renew = 1;


-- 12. Orphan entitlements
SELECT e.entitlement_id
FROM entitlements e
LEFT JOIN users u
    ON e.user_id = u.user_id
WHERE u.user_id IS NULL;


-- 13. Entitlements for invalid courses
SELECT e.entitlement_id
FROM entitlements e
LEFT JOIN courses c
    ON e.course_id = c.course_id
WHERE c.course_id IS NULL;


-- 14. Entitlements for invalid subscriptions
SELECT e.entitlement_id
FROM entitlements e
LEFT JOIN subscriptions s
    ON e.subscription_id = s.subscription_id
WHERE s.subscription_id IS NULL;


-- 15. Entitlement user mismatch
SELECT e.entitlement_id
FROM entitlements e
JOIN subscriptions s
    ON e.subscription_id = s.subscription_id
WHERE e.user_id != s.user_id;


-- 16. Duplicate active course entitlements
SELECT
    user_id,
    course_id,
    COUNT(*) AS entitlement_count
FROM entitlements
WHERE revoked_at IS NULL
GROUP BY user_id, course_id
HAVING COUNT(*) > 1;


-- 17. Successful payment with missing paid timestamp
SELECT payment_id
FROM payments
WHERE status = 'success'
AND paid_at IS NULL;


-- 18. Payment amount below zero
SELECT payment_id
FROM payments
WHERE amount < 0;


-- 19. Duplicate transaction IDs
SELECT
    transaction_id,
    COUNT(*) AS transaction_count
FROM payments
GROUP BY transaction_id
HAVING COUNT(*) > 1;


-- 20. Inactive user with active subscription
SELECT s.subscription_id
FROM subscriptions s
JOIN users u
    ON s.user_id = u.user_id
WHERE u.is_active = 0
AND s.status = 'active';