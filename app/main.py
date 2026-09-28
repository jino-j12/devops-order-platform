import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.metrics import router as metrics_router
from app.api.orders import router as orders_router
from app.api.products import router as products_router
from app.database.base import Base
from app.database.session import engine

logger = logging.getLogger("app")

app = FastAPI(title="DevOps Order Platform")

Base.metadata.create_all(bind=engine)

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(metrics_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error while processing %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health_check():
    from sqlalchemy import text

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "database healthy"}
