from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..dto.order_dto import AddOrderedGoodRequest, AddOrderedGoodResponse
from ..services.order_service import OrderService
from ...domain.repositories.order_repository import OrderRepository
from ...infrastructure.repositories.order_repository_impl import OrderRepositoryImpl


def get_order_repository() -> OrderRepository:
    """Dependency для получения репозитория заказов"""
    return OrderRepositoryImpl()


def get_order_service(
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)]
) -> OrderService:
    """Dependency для получения сервиса заказов"""
    return OrderService(order_repository)


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/add-good",
    response_model=AddOrderedGoodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить товар в заказ",
    description="Добавляет товар в существующий заказ с указанным количеством"
)
async def add_good_to_order(
    request: AddOrderedGoodRequest,
    order_service: Annotated[OrderService, Depends(get_order_service)]
) -> AddOrderedGoodResponse:
    """
    Добавить товар в заказ
    
    - **order_id**: ID существующего заказа
    - **good_id**: ID товара для добавления
    - **amount**: Количество товара (должно быть больше 0)
    
    Возвращает результат операции с детальной информацией.
    """
    try:
        response = await order_service.add_ordered_good(request)
        
        if not response.success:
            if "не найден" in response.message:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=response.message
                )
            elif "Недостаточно товара" in response.message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=response.message
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=response.message
                )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )
