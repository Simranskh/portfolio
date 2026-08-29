## 🔍 Modules Tested

### 🔐 Authentication & Users

- Valid login
- Invalid login
- Logout
- Create user
- Duplicate email validation
- Retrieve existing user

### 📋 Subscription

- Create subscription
- Retrieve subscription
- Duplicate active subscription
- Cancel subscription
- Subscription expiry

### 💳 Payments

- Successful payment
- Payment amount validation
- Payment history
- Transaction validation

### 📚 Courses

- List courses
- Retrieve course

### 🔑 Access Control

- Grant course access
- Verify course access
- Deny access without entitlement
- Deny access after subscription expiry

### 🗄️ Database Integrity

- Orphan subscription validation
- Invalid plan references
- Orphan payment validation
- Payment/user consistency
- Invalid plan prices
- Subscription status validation
- Orphan entitlement validation
- Payment timestamp validation

---

## 🧪 Automation Architecture

    Pytest Test
         ↓
    Pytest Fixture
         ↓
    API Client
         ↓
    FastAPI TestClient
         ↓
    REST API
         ↓
    SQLite Database

The framework uses dedicated API client classes and reusable Pytest fixtures to keep test logic clean and maintainable.

---

## 🔄 Subscription Workflow

    User
     ↓
    Select Plan
     ↓
    Create Subscription
     ↓
    Payment
     ↓
    Entitlement
     ↓
    Course Access
     ↓
    Cancel / Expire
     ↓
    Access Denied

---

## ▶️ How to Run

### 1. Activate Virtual Environment

    .\.venv\Scripts\Activate.ps1

### 2. Navigate to Project

    cd E:\Portfolio\05-education-subscription-saas

### 3. Initialize Database

    python database\init_db.py

### 4. Run Tests

    pytest

For verbose execution:

    pytest -v

---

## ✅ Latest Test Result

    ============================ 28 passed, 0 warnings ============================

### Final Status

**28 / 28 tests passed**

**0 failures**

---

## 🎓 QA Skills Demonstrated

- API Testing
- REST API Automation
- Python
- Pytest
- FastAPI
- API Client Framework
- Pytest Fixtures
- Positive Testing
- Negative Testing
- Business Rule Testing
- Authentication Testing
- Authorization Testing
- Subscription Lifecycle Testing
- Payment Testing
- Database Testing
- SQL Validation
- Referential Integrity
- Test Data Management
- Regression Testing
- CI/CD
- GitHub Actions

---

## 🚀 Future Enhancements

- HTML / Allure reports
- API schema validation
- Parameterized tests
- Test data factories
- Docker integration
- API performance testing
- Expanded CI/CD reporting

---

## 👤 Author

**Simran**

QA / Software Testing Portfolio Project

---

⭐ **Focus:** API Automation • Python • Pytest • FastAPI • Database QA • SQL • Subscription Testing • Access Control • CI/CD