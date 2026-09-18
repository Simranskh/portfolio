# Digital Library API Testing — REST API Automation

A Python-based API automation project for testing a Digital Library backend.  
The project validates Books, Members, and Borrow/Return workflows through automated REST API tests with database validation.

## 🎯 Project Objective

The goal of this project is to validate the functional behavior, negative scenarios, business rules, and database state of a Digital Library API.

The automation suite verifies both:

- API response behavior
- Backend database state after API operations

---

## 🧪 QA Coverage

### Books API
- Create book
- Get book by ID
- Update book
- Delete book
- Duplicate ISBN validation
- Invalid book ID validation
- Database validation after create/update/delete

### Members API
- Create member
- Get member by ID
- Duplicate email validation
- Invalid member ID validation
- Database validation

### Borrow & Return API
- Borrow a book
- Return a book
- Invalid book validation
- Invalid member validation
- Prevent borrowing an already borrowed book
- Prevent returning an already returned book
- Invalid borrow ID validation
- Database validation of borrow/return status
- Book availability validation

### API Validation
- HTTP status code validation
- JSON response validation
- Success and error response validation
- Negative API testing
- Business-rule validation

### Database Validation
- SQLite database validation
- Verify created records
- Verify updated records
- Verify deleted records
- Verify borrow records
- Verify book availability state

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Automation language |
| Pytest | Test framework |
| HTTPX | API requests |
| FastAPI | Backend application |
| SQLite | Database |
| Allure | Test reporting |
| Git | Version control |
| GitHub | Source code management |

---

## 📁 Project Structure

```text
02-digital-library-api-testing/
│
├── app/
│   ├── backend/
│   │   ├── books.py
│   │   ├── borrow.py
│   │   ├── main.py
│   │   └── members.py
│   │
│   └── database/
│       ├── init_db.py
│       ├── library.db
│       └── schema.sql
│
├── automation/
│   ├── api/
│   │   ├── books_api.py
│   │   ├── borrow_api.py
│   │   └── members_api.py
│   │
│   ├── fixtures/
│   │   └── api_fixtures.py
│   │
│   ├── tests/
│   │   ├── test_books_api.py
│   │   ├── test_borrow_api.py
│   │   └── test_members_api.py
│   │
│   ├── utils/
│   │   └── db_utils.py
│   │
│   └── config.py
│
├── conftest.py
├── README.md
└── .gitignore
Allure Report :
![Allure Test Report] (screenshot/AllureP2.png)