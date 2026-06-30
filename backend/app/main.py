from fastapi import Depends, FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .database import Base, engine
from .routers import transactions, ai
from .dependencies import require_auth
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(dependencies=[Depends(require_auth)])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(transactions.router)
app.include_router(ai.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8082",
        "http://192.168.178.71:8082",
        "https://spending.dylanvdk.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Spending tracker API is running"}