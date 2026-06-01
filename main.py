from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from middleware import configure_middleware
from employees.router import router as employee_router
from auth.router import router as auth_router
from addresses.router import router as address_router
from departments.router import router as department_router
from config import settings
from exceptions.handler import register_exception_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await
    yield


app = FastAPI(title="Employee App", description="Simple Employee App", version="1.0.0", lifespan=lifespan)

configure_middleware(app)
register_exception_handler(app)
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(address_router)
app.include_router(department_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "message": f"Employee CRUD API is running Environment : {settings.app_env}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.0", port=8000, reload=True)
