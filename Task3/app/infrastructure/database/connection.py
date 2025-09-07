import asyncio
import asyncpg
from typing import Optional
from contextlib import asynccontextmanager


class DatabaseConnection:
    """Сервис для подключения к PostgreSQL"""
    
    def __init__(self, host: str = "localhost", port: int = 5432, 
                 database: str = "postgres", user: str = "postgres", 
                 password: str = "postgres"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self._pool: Optional[asyncpg.Pool] = None
    
    async def create_pool(self, min_size: int = 10, max_size: int = 20) -> None:
        """Создать пул соединений"""
        self._pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            min_size=min_size,
            max_size=max_size
        )
    
    async def close_pool(self) -> None:
        """Закрыть пул соединений"""
        if self._pool:
            await self._pool.close()
    
    @asynccontextmanager
    async def get_connection(self):
        """Получить соединение из пула"""
        if not self._pool:
            raise RuntimeError("Database pool is not initialized. Call create_pool() first.")
        
        async with self._pool.acquire() as connection:
            yield connection
    
    async def execute_query(self, query: str, *args) -> list:
        """Выполнить запрос и вернуть результат"""
        async with self.get_connection() as conn:
            return await conn.fetch(query, *args)
    
    async def execute_command(self, command: str, *args) -> str:
        """Выполнить команду (INSERT, UPDATE, DELETE)"""
        async with self.get_connection() as conn:
            return await conn.execute(command, *args)
    
    async def fetch_one(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Выполнить запрос и вернуть одну запись"""
        async with self.get_connection() as conn:
            return await conn.fetchrow(query, *args)
    
    async def fetch_val(self, query: str, *args) -> Optional[any]:
        """Выполнить запрос и вернуть одно значение"""
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)


# Глобальный экземпляр подключения к БД
db_connection = DatabaseConnection()
