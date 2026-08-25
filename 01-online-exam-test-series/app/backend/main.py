from fastapi import FastAPI
from auth import router as auth_router
from test_series import router as test_series_router
from questions import router as questions_router
from exam_attempt import router as exam_attempt_router
from attempt_answers import router as attempt_answers_router
app = FastAPI(title="ExamPro API")

app.include_router(questions_router)
app.include_router(auth_router)
app.include_router(test_series_router)
app.include_router(exam_attempt_router)
app.include_router(attempt_answers_router)

@app.get("/")
def root():
    return {
        "application": "ExamPro",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }