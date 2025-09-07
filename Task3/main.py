import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.application.controllers.order_controller import router as order_router
from app.infrastructure.database.connection import db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Инициализация при запуске
    await db_connection.create_pool()
    print("Database connection pool created")
    
    yield
    
    # Очистка при завершении
    await db_connection.close_pool()
    print("Database connection pool closed")


# Создание экземпляра FastAPI
app = FastAPI(
    title="Order API",
    description="REST API для добавления заказа по ID",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(order_router)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Order Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Проверка состояния приложения"""
    try:
        # Проверяем подключение к БД
        await db_connection.fetch_val("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
