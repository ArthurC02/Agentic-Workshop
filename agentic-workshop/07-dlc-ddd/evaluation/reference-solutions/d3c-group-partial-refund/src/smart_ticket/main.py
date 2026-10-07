from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from smart_ticket.api.routes import router
from smart_ticket.domain.errors import DomainError

app = FastAPI(title="Smart Ticket Platform", version="1.7.0")
app.include_router(router)

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code,
                        content={"error": {"code": exc.code, "message": exc.message}})

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    code = "NOT_IMPLEMENTED" if exc.status_code == 501 else "HTTP_ERROR"
    return JSONResponse(status_code=exc.status_code,
                        content={"error": {"code": code, "message": str(exc.detail)}})

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
