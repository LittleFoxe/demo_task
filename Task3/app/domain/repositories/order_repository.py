from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.order import Order, OrderedGood, Good


class OrderRepository(ABC):
    """Абстрактный репозиторий для работы с заказами"""
    
    @abstractmethod
    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Получить заказ по ID"""
        pass
    
    @abstractmethod
    async def get_ordered_goods_by_order_id(self, order_id: int) -> List[OrderedGood]:
        """Получить товары в заказе по ID заказа"""
        pass
    
    @abstractmethod
    async def get_good_by_id(self, good_id: int) -> Optional[Good]:
        """Получить товар по ID"""
        pass
    
    @abstractmethod
    async def add_ordered_good(self, ordered_good: OrderedGood) -> bool:
        """Добавить товар в заказ"""
        pass
    
    @abstractmethod
    async def update_ordered_good(self, ordered_good: OrderedGood) -> bool:
        """Обновить товар в заказе"""
        pass
    
    @abstractmethod
    async def delete_ordered_good(self, order_id: int, good_id: int) -> bool:
        """Удалить товар из заказа"""
        pass
