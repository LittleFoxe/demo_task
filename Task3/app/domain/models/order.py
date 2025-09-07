from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    """Модель заказа"""
    id: int
    client_id: int
    
    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("Order ID must be positive")
        if self.client_id <= 0:
            raise ValueError("Client ID must be positive")


@dataclass
class OrderedGood:
    """Модель товара в заказе"""
    order_id: int
    good_id: int
    amount: int
    
    def __post_init__(self):
        if self.order_id <= 0:
            raise ValueError("Order ID must be positive")
        if self.good_id <= 0:
            raise ValueError("Good ID must be positive")
        if self.amount <= 0:
            raise ValueError("Amount must be positive")


@dataclass
class Good:
    """Модель товара"""
    id: int
    name: str
    amount: int
    price: float
    catalogue_id: Optional[int] = None
    
    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("Good ID must be positive")
        if not self.name or not self.name.strip():
            raise ValueError("Good name cannot be empty")
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.catalogue_id is not None and self.catalogue_id <= 0:
            raise ValueError("Catalogue ID must be positive")


@dataclass
class Client:
    """Модель клиента"""
    id: int
    name: str
    address: Optional[str] = None
    
    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("Client ID must be positive")
        if not self.name or not self.name.strip():
            raise ValueError("Client name cannot be empty")
