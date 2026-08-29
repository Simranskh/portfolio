# 📊 Student Performance Dashboard — SQL QA & Reporting

A database QA and analytics project designed around an online student examination system.  
The project uses **SQLite, SQL, and Python** to validate relational data, test business rules, and generate student performance reports.

---

## 🎯 Project Objective

This project demonstrates practical **Database QA + SQL Testing + Reporting** skills by:

- Validating database integrity
- Testing relational data
- Detecting invalid or inconsistent records
- Validating business rules
- Performing boundary and negative testing
- Generating analytical reports
- Automating SQL execution using Python
- Verifying query execution results

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **SQLite** | Database |
| **SQL** | QA validation & reporting |
| **Python** | SQL automation |
| **sqlite3** | Python database connectivity |
| **PyCharm** | Development environment |
| **Git / GitHub** | Version control |

---

## 📁 Project Structure

```text
04-student-performance-dashboard/
│
├── run_queries.py
│
├── database/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── student_performance.db
│
└── sql/
    ├── qa_validation.sql
    └── reporting_queries.sql
```

---

## 🗄️ Database Overview

The database represents a simplified online examination and student performance system.

### Main Entities

- Students
- Subjects
- Tests
- Questions
- Attempts
- Question-level attempt data

### Relationships

```text
Students
   │
   └── Attempts
          │
          └── Tests
                │
                ├── Subjects
                │
                └── Questions
```

This structure allows performance to be analyzed from **student level down to individual question level**.

---

# 🔍 SQL QA Validation

The `qa_validation.sql` file contains database validation queries designed to identify data integrity and business-rule issues.

### Validations Include

- Orphan attempts referencing invalid students
- Orphan attempts referencing invalid tests
- Scores greater than total marks
- Incorrect pass/fail status
- Attempt marks inconsistent with test marks
- Questions referencing invalid tests
- Invalid relational mappings
- Data consistency checks
- Pass/fail calculation checks
- Score percentage validation

### QA Result

```text
QA validations executed: 16
QA validations failed:    0
```

All database QA validations currently pass successfully.

---

# 📊 SQL Reporting

The `reporting_queries.sql` file contains **30 analytical SQL queries**.

### Reporting Areas

#### 👨‍🎓 Student Performance
- Student ranking
- Average score
- Highest score
- Lowest score
- Pass/fail statistics
- Performance percentage

#### 📚 Subject Analysis
- Subject-wise attempts
- Average scores
- Highest/lowest scores
- Pass/fail distribution
- Subject comparison

#### 📝 Test Analysis
- Test-type performance
- Test-level statistics
- Average scores
- Pass/fail results
- Test difficulty analysis

#### 📈 Attempt Analysis
- Attempt history
- Score progression
- Improvement/decline
- Detailed attempt performance

#### ❓ Question Analysis
- Question difficulty
- Correct/incorrect answers
- Question-level performance
- Difficulty distribution

#### 📊 Overall Analytics
- Total attempts
- Total marks
- Obtained marks
- Overall performance percentage

---

# 🤖 Python SQL Automation

The `run_queries.py` script automates the complete database QA and reporting workflow.

### Automation Flow

```text
SQLite Database
       ↓
QA Validation Queries
       ↓
Validate Database Integrity
       ↓
Reporting Queries
       ↓
Generate Analytics
       ↓
Track Query Results
       ↓
Final Pass/Fail Result
```

The Python script:

1. Connects to `student_performance.db`
2. Loads QA validation queries
3. Executes each validation
4. Checks returned rows
5. Loads reporting queries
6. Executes each report
7. Displays query results
8. Tracks failures
9. Generates the final execution status

---

# ▶️ How to Run

### 1. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If the environment is already active, skip this step.

### 2. Navigate to the Project

```powershell
cd E:\Portfolio\04-student-performance-dashboard
```

### 3. Run the Complete QA + Reporting Suite

```powershell
python run_queries.py
```

---

# ✅ Latest Execution Result

```text
============================================================
STUDENT PERFORMANCE DATABASE
QA + REPORTING EXECUTION
============================================================

QA validations executed: 16
QA validations failed:    0

Reports executed:        30
Reports failed:           0

Total queries executed:  46
Total failures:           0

============================================================
RESULT: ALL QA + REPORTING QUERIES PASSED
============================================================
```

### Final Status

**46 / 46 queries passed**

**0 failures**

---

# 🧪 QA Testing Approach

The project applies multiple database testing techniques.

### 1. Referential Integrity Testing

Checks whether foreign-key relationships reference valid records.

```sql
SELECT
    a.attempt_id,
    a.student_id
FROM attempts a
LEFT JOIN students s
    ON a.student_id = s.student_id
WHERE s.student_id IS NULL;
```

Expected result:

```text
0 rows
```

### 2. Business Rule Testing

Validates whether the stored attempt status matches the configured pass marks.

```sql
WHERE
    (a.score >= t.pass_marks AND a.status != 'passed')
    OR
    (a.score < t.pass_marks AND a.status != 'failed');
```

Expected result:

```text
0 rows
```

### 3. Boundary Testing

Checks whether a score exceeds the maximum possible marks.

```sql
WHERE score > total_marks;
```

Expected result:

```text
0 rows
```

### 4. Cross-Table Consistency

Checks whether attempt marks match the corresponding test configuration.

```sql
WHERE a.total_marks != t.total_marks;
```

Expected result:

```text
0 rows
```

### 5. Analytical Validation

Reporting queries are executed against the validated database to ensure that reliable business analytics can be generated from the underlying data.

---

# 💡 Business Questions Answered

The reporting layer can answer questions such as:

### Who are the highest-performing students?

Students can be ranked using average scores, pass rates, and performance percentages.

### Which subject performs best?

Subject-level reports compare:

- Attempts
- Average score
- Highest score
- Lowest score
- Pass/fail performance

### Which tests perform best?

Test reports compare:

- Test type
- Number of attempts
- Average score
- Maximum score
- Minimum score
- Pass/fail results

### Are students improving?

Attempt-history reports compare consecutive attempts and identify:

- First attempt
- Improved performance
- Declined performance

### Which questions are difficult?

Question-level reports analyze:

- Correct answers
- Incorrect answers
- Accuracy
- Difficulty classification
- Difficulty distribution

---

# 📈 Sample Analytics

The current dataset contains:

```text
Students: 5
Subjects: 3
Tests: 9
Attempts: 25
```

The reporting layer generates analytics across student, subject, test, attempt, and question levels.

---

# 🎓 QA Skills Demonstrated

This project demonstrates practical experience with:

- SQL Testing
- Database Testing
- SQLite
- Data Validation
- Referential Integrity Testing
- Business Rule Testing
- Boundary Testing
- Negative Testing
- Relational Joins
- GROUP BY
- HAVING
- CASE Expressions
- Subqueries
- CTEs
- Window Functions
- Aggregations
- Analytical SQL
- Test Data Validation
- Python SQL Automation
- Query Result Validation
- Regression-style Database Testing
- Reporting & Analytics

---

# 🚀 Future Enhancements

Planned improvements can include:

- Pytest-based database test framework
- HTML test reports
- Automated test-result artifacts
- GitHub Actions CI/CD
- Database test fixtures
- Negative test-data generation
- REST API integration
- Interactive dashboard
- Automated database quality reports

---

# 📌 Project Summary

This project demonstrates how SQL can be used not only for reporting, but also as a **database QA and validation tool**.

```text
Database
   ↓
Test Data
   ↓
SQL QA Validation
   ↓
Python Automation
   ↓
Reporting Queries
   ↓
Validated Analytics
```

### Current Implementation

```text
16 QA validations
        +
30 reporting queries
        =
46 automated SQL checks/reports

46 PASSED
0 FAILED
```

---

## 👤 Author

**Simran**

QA / Software Testing Portfolio Project

---

⭐ **Focus:** Database QA • SQL Testing • Data Validation • Reporting • Python Automation