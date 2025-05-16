from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meow_bank.api.routes import accounts, customers, transfers
from meow_bank.api.security import get_api_key
from meow_bank.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Meow Bank API",
    description="A banking API for managing accounts and transfers",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(dependencies=[Depends(get_api_key)], prefix="/api")

router.include_router(customers.router)
router.include_router(accounts.router)
router.include_router(transfers.router)

app.include_router(router)
