from pydantic import BaseModel, Field
from typing import Optional


class AddOrderedGoodRequest(BaseModel):
    """DTO для добавления товара в заказ"""
    order_id: int = Field(..., gt=0, description="ID заказа")
    good_id: int = Field(..., gt=0, description="ID товара")
    amount: int = Field(..., gt=0, description="Количество товара")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "good_id": 5,
                "amount": 2
            }
        }


class AddOrderedGoodResponse(BaseModel):
    """DTO для ответа при добавлении товара в заказ"""
    success: bool = Field(..., description="Успешность операции")
    message: str = Field(..., description="Сообщение о результате")
    order_id: Optional[int] = Field(None, description="ID заказа")
    good_id: Optional[int] = Field(None, description="ID товара")
    amount: Optional[int] = Field(None, description="Количество товара")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Товар успешно добавлен в заказ",
                "order_id": 1,
                "good_id": 5,
                "amount": 2
            }
        }


class ErrorResponse(BaseModel):
    """DTO для ошибок"""
    success: bool = Field(False, description="Успешность операции")
    message: str = Field(..., description="Сообщение об ошибке")
    error_code: Optional[str] = Field(None, description="Код ошибки")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Заказ не найден",
                "error_code": "ORDER_NOT_FOUND"
            }
        }
