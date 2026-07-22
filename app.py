from fastapi import FastAPI
from presentation.api.books import router as books_router
from presentation.api.users import router as users_router
from presentation.api.copies import router as copy_router
from presentation.api.loans import router as loans_router
from presentation.exception_handlers.handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.include_router(books_router)
app.include_router(copy_router)
app.include_router(users_router)
app.include_router(loans_router)
