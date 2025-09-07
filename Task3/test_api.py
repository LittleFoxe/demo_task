#!/usr/bin/env python3
"""
Простой тестовый скрипт для проверки работы API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_add_good_to_order():
    """Тест добавления товара в заказ"""
    url = f"{BASE_URL}/orders/add-good"
    
    # Тест 1: Добавление товара в существующий заказ
    print("Тест 1: Добавление товара в заказ")
    data = {
        "order_id": 1,
        "good_id": 5,
        "amount": 2
    }
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
    print()
    
    # Тест 2: Добавление того же товара (должно увеличить количество)
    print("Тест 2: Добавление того же товара (увеличение количества)")
    data = {
        "order_id": 1,
        "good_id": 5,
        "amount": 1
    }
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
    print()
    
    # Тест 3: Попытка добавить несуществующий заказ
    print("Тест 3: Несуществующий заказ")
    data = {
        "order_id": 99999,
        "good_id": 5,
        "amount": 1
    }
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
    print()
    
    # Тест 4: Попытка добавить несуществующий товар
    print("Тест 4: Несуществующий товар")
    data = {
        "order_id": 1,
        "good_id": 99999,
        "amount": 1
    }
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
    print()
    
    # Тест 5: Попытка добавить больше товара, чем есть на складе
    print("Тест 5: Недостаточно товара на складе")
    data = {
        "order_id": 1,
        "good_id": 5,
        "amount": 1000
    }
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
    print()
    
    # Тест 6: Демонстрация уменьшения количества на складе
    print("Тест 6: Демонстрация уменьшения количества на складе")
    print("Добавляем товар несколько раз, чтобы показать уменьшение остатка...")
    
    for i in range(3):
        data = {
            "order_id": 2,
            "good_id": 1,  # Стиральная машина Bosch (изначально 5 штук)
            "amount": 1
        }
        
        response = requests.post(url, json=data)
        print(f"Попытка {i+1}: Статус {response.status_code}, Ответ: {response.json()}")
    
    print()

def test_health_check():
    """Тест проверки состояния API"""
    print("Тест проверки состояния API")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}")
    print()

if __name__ == "__main__":
    print("Запуск тестов API...")
    print("=" * 50)
    
    try:
        test_health_check()
        test_add_good_to_order()
        print("Все тесты завершены!")
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удается подключиться к API. Убедитесь, что сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"Ошибка: {e}")
