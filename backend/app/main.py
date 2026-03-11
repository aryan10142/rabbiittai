from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes import router, limiter
from app.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Sales Insight Automator API",
        description=(
            "Upload sales data (.csv/.xlsx) and receive an AI-generated executive "
            "summary delivered straight to your inbox.\n\n"
            "**Security features:** CORS whitelisting, rate limiting, file-type "
            "validation, file-size caps, and input sanitization."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # --- Middleware ---
    origins = [o.strip() for o in settings.allowed_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # --- Rate limiter ---
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # --- Routes ---
    app.include_router(router, prefix="/api")

    return app


app = create_app()
