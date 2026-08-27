\# Quiz Practice API – API Automation \& CI/CD



A backend API testing project built with \*\*FastAPI, SQLite, Python, Pytest, Requests, and GitHub Actions\*\*.



This project demonstrates REST API validation, database-backed API behavior, automated API testing, and continuous integration using GitHub Actions.



\---



\## 🎯 Project Objective



The goal of this project is to build and automate testing for a quiz management REST API.



The automation validates:



\- Quiz creation

\- Quiz retrieval

\- Quiz retrieval by ID

\- Invalid quiz handling

\- Question creation

\- Invalid quiz handling while creating questions

\- Question retrieval

\- Quiz attempt submission

\- HTTP status codes

\- JSON response structure

\- Response data validation

\- Database initialization

\- Automated CI execution



\---



\## 🛠️ Tech Stack



| Technology | Purpose |

|---|---|

| Python 3.13 | Programming language |

| FastAPI | Backend REST API |

| SQLite | Database |

| Pytest | Test framework |

| Requests | API automation |

| Git | Version control |

| GitHub Actions | CI/CD automation |



\---



\## 📁 Project Structure



```text

03-quiz-practice-ci-cd/

│

├── app/

│   ├── backend/

│   │   └── main.py

│   │

│   └── database/

│       ├── init\_db.py

│       └── schema.sql

│

├── automation/

│   ├── api/

│   │   └── quizzes\_api.py

│   │

│   ├── fixtures/

│   │   └── api\_fixtures.py

│   │

│   ├── tests/

│   │   └── test\_quizzes\_api.py

│   │

│   └── config.py

│

├── .gitignore

├── conftest.py

├── requirements.txt

└── README.md

## 🔌 API Coverage



\### Quiz APIs



| Method | Endpoint | Purpose |

|---|---|---|

| POST | `/api/quizzes` | Create a quiz |

| GET | `/api/quizzes` | Get all quizzes |

| GET | `/api/quizzes/{quiz\_id}` | Get quiz by ID |



\### Question APIs



| Method | Endpoint | Purpose |

|---|---|---|

| POST | `/api/quizzes/{quiz\_id}/questions` | Create a question |

| GET | `/api/quizzes/{quiz\_id}/questions` | Get quiz questions |



\### Attempt API



| Method | Endpoint | Purpose |

|---|---|---|

| POST | `/api/quizzes/{quiz\_id}/attempt` | Submit a quiz attempt |

