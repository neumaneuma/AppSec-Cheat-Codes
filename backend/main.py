import logging
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from backend.constants import SESSION_IDENTIFIER
from backend.database import reset_db
from backend.helper import timing_safe_compare
from backend.passphrases import Passphrases
from backend.patches.sqli_login_bypass import router as sqli_login_bypass_patched_router
from backend.patches.sqli_second_order import router as sqli_second_order_patched_router
from backend.patches.ssrf_lfi import router as ssrf_lfi_patched_router
from backend.patches.ssrf_webhook import router as ssrf_webhook_patched_router
from backend.vulnerabilities.sqli_login_bypass import (
    router as sqli_login_bypass_vulnerable_router,
)
from backend.vulnerabilities.sqli_second_order import (
    router as sqli_second_order_vulnerable_router,
)
from backend.vulnerabilities.ssrf_lfi import router as ssrf_lfi_vulnerable_router
from backend.vulnerabilities.ssrf_webhook import (
    router as ssrf_webhook_vulnerable_router,
)

# Initialize app
app = FastAPI()
app.add_middleware(
    SessionMiddleware, secret_key=secrets.token_hex(), session_cookie=SESSION_IDENTIFIER
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ctf.neumaneuma.com", "http://localhost:12300"],
    # Carve out a wildcard SOP exception for my Cloudflare Pages dev sites
    allow_origin_regex=r"https://.*\.appseccheatcodes\.pages\.dev",
    allow_credentials=True,
    allow_methods=["POST", "GET"],
)
app.include_router(sqli_login_bypass_vulnerable_router)
app.include_router(sqli_second_order_vulnerable_router)
app.include_router(ssrf_webhook_vulnerable_router)
app.include_router(ssrf_lfi_vulnerable_router)
app.include_router(sqli_login_bypass_patched_router)
app.include_router(sqli_second_order_patched_router)
app.include_router(ssrf_webhook_patched_router)
app.include_router(ssrf_lfi_patched_router)
reset_db()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Business logic error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if request.client is None:
        logger.info(
            f'"{request.method} {request.url.path} HTTP/1.1" '
            f"{exc.status_code} - {exc.detail}"
        )
    else:
        logger.info(
            f"{request.client.host}:{request.client.port} - "
            f'"{request.method} {request.url.path} HTTP/1.1" '
            f"{exc.status_code} - {exc.detail}"
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Pydantic error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    if request.client is None:
        logger.info(
            f'"{request.method} {request.url.path} HTTP/1.1" 422 - {exc.errors()}'
        )
    else:
        logger.info(
            f"{request.client.host}:{request.client.port} - "
            f'"{request.method} {request.url.path} HTTP/1.1" '
            f"422 - {exc.errors()}"
        )
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


class Flag(BaseModel):
    secret: str
    challenge: str


@app.get("/")
async def root() -> str:
    return "👋 🌎"


@app.get("/health")
async def health() -> str:
    return "OK"


@app.post("/submission")
async def submission(flag: Flag) -> dict[str, bool | str]:
    match flag.challenge:
        case Passphrases.sqli1.name:
            expected = Passphrases.sqli1.value
        case Passphrases.sqli2.name:
            expected = Passphrases.sqli2.value
        case Passphrases.ssrf1.name:
            expected = Passphrases.ssrf1.value
        case Passphrases.ssrf2.name:
            expected = Passphrases.ssrf2.value
        case _:
            return {"result": False, "message": "Invalid challenge"}

    return {"result": timing_safe_compare(flag.secret, expected)}
