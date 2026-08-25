from fastapi import FastAPI

from app.backend.books import router as books_router
from app.backend.members import router as members_router
from app.backend.borrow import router as borrow_router


app = FastAPI(title="Digital Library API")


app.include_router(books_router)
app.include_router(members_router)
app.include_router(borrow_router)


@app.get("/")
def root():
    return {
        "application": "Digital Library API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }