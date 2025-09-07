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
                    message="Заказ не найден"
                )
            
            # Проверяем существование товара
            good = await self.order_repository.get_good_by_id(request.good_id)
            if not good:
                return AddOrderedGoodResponse(
                    success=False,
                    message="Товар не найден"
                )
            
            # Проверяем наличие товара на складе
            if good.amount < request.amount:
                return AddOrderedGoodResponse(
                    success=False,
                    message=f"Недостаточно товара на складе. Доступно: {good.amount}, запрошено: {request.amount}"
                )
            
            # Проверяем, есть ли уже такой товар в заказе
            existing_ordered_goods = await self.order_repository.get_ordered_goods_by_order_id(request.order_id)
            existing_good = next((og for og in existing_ordered_goods if og.good_id == request.good_id), None)
            
            # Уменьшаем количество товара на складе
            new_stock_amount = good.amount - request.amount
            stock_updated = await self.order_repository.update_good_amount(request.good_id, new_stock_amount)
            
            if not stock_updated:
                return AddOrderedGoodResponse(
                    success=False,
                    message="Ошибка при обновлении количества товара на складе"
                )
            
            if existing_good:
                # Если товар уже есть в заказе, увеличиваем количество
                new_amount = existing_good.amount + request.amount
                updated_ordered_good = OrderedGood(
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=new_amount
                )
                success = await self.order_repository.update_ordered_good(updated_ordered_good)
                message = f"Количество товара в заказе увеличено. Новое количество: {new_amount}. Остаток на складе: {new_stock_amount}"
            else:
                # Если товара нет в заказе, добавляем новый
                ordered_good = OrderedGood(
                    order_id=request.order_id,
                    good_id=request.good_id,
                    amount=request.amount
                )
                success = await self.order_repository.add_ordered_good(ordered_good)
                message = f"Товар успешно добавлен в заказ. Остаток на складе: {new_stock_amount}"
            
            if success:
                return AddOrderedGoodResponse(
                    success=True,
                    message=message
                )
            else:
                return AddOrderedGoodResponse(
                    success=False,
                    message="Ошибка при добавлении товара в заказ"
                )
                
        except Exception as e:
            return AddOrderedGoodResponse(
                success=False,
                message=f"Внутренняя ошибка сервера: {str(e)}"
            )
