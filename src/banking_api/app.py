"""Main FastAPI application.

This module creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import transactions, stats, fraud, customers, system
from .utils.data_loader import DataLoader


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for startup and shutdown events.

    Parameters
    ----------
    app : FastAPI
        FastAPI application instance.

    Yields
    ------
    None
        Control flow during application lifespan.
    """
    data_loader = DataLoader()
    try:
        data_loader.load_data()
        print("Dataset loaded successfully")
    except FileNotFoundError as e:
        print(f"Warning: {e}")
        print("API will start but some endpoints may fail")

    yield

    print("Shutting down application")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns
    -------
    FastAPI
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Banking Transactions API",
        description="API for exposing and analyzing banking transaction data",
        version="1.0.0",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(transactions.router)
    app.include_router(stats.router)
    app.include_router(fraud.router)
    app.include_router(customers.router)
    app.include_router(system.router)

    @app.get("/")
    def root() -> dict:
        """Root endpoint.

        Returns
        -------
        dict
            Welcome message with API information.
        """
        return {
            "message": "Banking Transactions API",
            "version": "1.0.0",
            "docs": "/docs"
        }

    return app


app = create_app()
