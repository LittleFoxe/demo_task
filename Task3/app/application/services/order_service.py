from typing import Optional
from ...domain.models.order import Order, OrderedGood, Good
from ...domain.repositories.order_repository import OrderRepository
from ..dto.order_dto import AddOrderedGoodRequest, AddOrderedGoodResponse, ErrorResponse


class OrderService:
    """Сервис для работы с заказами"""
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    async def add_ordered_good(self, request: AddOrderedGoodRequest) -> AddOrderedGoodResponse:
        """Добавить товар в заказ"""
        try:
            # Проверяем существование заказа
            order = await self.order_repository.get_order_by_id(request.order_id)
            if not order:
                return AddOrderedGoodResponse(
                    success=False,
                    message="Заказ не найден",
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=request.amount
                )
            
            # Проверяем существование товара
            good = await self.order_repository.get_good_by_id(request.good_id)
            if not good:
                return AddOrderedGoodResponse(
                    success=False,
                    message="Товар не найден",
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=request.amount
                )
            
            # Проверяем наличие товара на складе
            if good.amount < request.amount:
                return AddOrderedGoodResponse(
                    success=False,
                    message=f"Недостаточно товара на складе. Доступно: {good.amount}, запрошено: {request.amount}",
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=request.amount
                )
            
            # Создаем объект товара в заказе
            ordered_good = OrderedGood(
                order_id=request.order_id,
                good_id=request.good_id,
                amount=request.amount
            )
            
            # Добавляем товар в заказ
            success = await self.order_repository.add_ordered_good(ordered_good)
            
            if success:
                return AddOrderedGoodResponse(
                    success=True,
                    message="Товар успешно добавлен в заказ",
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=request.amount
                )
            else:
                return AddOrderedGoodResponse(
                    success=False,
                    message="Ошибка при добавлении товара в заказ",
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=request.amount
                )
                
        except Exception as e:
            return AddOrderedGoodResponse(
                success=False,
                message=f"Внутренняя ошибка сервера: {str(e)}",
                order_id=request.order_id,
                good_id=request.good_id,
                amount=request.amount
            )
