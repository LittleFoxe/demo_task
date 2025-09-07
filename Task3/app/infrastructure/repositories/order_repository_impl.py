from typing import List, Optional
from decimal import Decimal
from ...domain.models.order import Order, OrderedGood, Good
from ...domain.repositories.order_repository import OrderRepository
from ..database.connection import db_connection


class OrderRepositoryImpl(OrderRepository):
    """Реализация репозитория для работы с заказами"""
    
    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Получить заказ по ID"""
        query = "SELECT id, client_id FROM Orders WHERE id = $1"
        row = await db_connection.fetch_one(query, order_id)
        
        if row:
            return Order(id=row['id'], client_id=row['client_id'])
        return None
    
    async def get_ordered_goods_by_order_id(self, order_id: int) -> List[OrderedGood]:
        """Получить товары в заказе по ID заказа"""
        query = """
            SELECT order_id, good_id, amount 
            FROM Ordered_goods 
            WHERE order_id = $1
        """
        rows = await db_connection.execute_query(query, order_id)
        
        return [
            OrderedGood(
                order_id=row['order_id'],
                good_id=row['good_id'],
                amount=row['amount']
            )
            for row in rows
        ]
    
    async def get_good_by_id(self, good_id: int) -> Optional[Good]:
        """Получить товар по ID"""
        query = """
            SELECT id, name, amount, price, catalogue_id 
            FROM Goods 
            WHERE id = $1
        """
        row = await db_connection.fetch_one(query, good_id)
        
        if row:
            return Good(
                id=row['id'],
                name=row['name'],
                amount=row['amount'],
                price=float(row['price']),
                catalogue_id=row['catalogue_id']
            )
        return None
    
    async def add_ordered_good(self, ordered_good: OrderedGood) -> bool:
        """Добавить товар в заказ"""
        query = """
            INSERT INTO Ordered_goods (order_id, good_id, amount)
            VALUES ($1, $2, $3)
            ON CONFLICT (order_id, good_id) 
            DO UPDATE SET amount = $3
        """
        try:
            await db_connection.execute_command(
                query, 
                ordered_good.order_id, 
                ordered_good.good_id, 
                ordered_good.amount
            )
            return True
        except Exception:
            return False
    
    async def update_ordered_good(self, ordered_good: OrderedGood) -> bool:
        """Обновить товар в заказе"""
        query = """
            UPDATE Ordered_goods 
            SET amount = $3 
            WHERE order_id = $1 AND good_id = $2
        """
        try:
            result = await db_connection.execute_command(
                query, 
                ordered_good.order_id, 
                ordered_good.good_id, 
                ordered_good.amount
            )
            return "UPDATE 1" in result
        except Exception:
            return False
    
    async def delete_ordered_good(self, order_id: int, good_id: int) -> bool:
        """Удалить товар из заказа"""
        query = """
            DELETE FROM Ordered_goods 
            WHERE order_id = $1 AND good_id = $2
        """
        try:
            result = await db_connection.execute_command(query, order_id, good_id)
            return "DELETE 1" in result
        except Exception:
            return False
