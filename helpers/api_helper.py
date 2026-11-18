import requests
import random

BASE_URL = "https://qa-stellarburgers.education-services.ru/api"

# ID ингредиентов из HTML-файла Stellar Burgers:
# 691577430cc94f001a65b859 — Краторная булка N-200i
# 691577430cc94f001a65b862 — Соус с шипами Антарианского плоскоходца
INGREDIENTS = ["691577430cc94f001a65b859", "691577430cc94f001a65b862"]


def generate_user_data():
    """Генерирует случайные данные для регистрации нового пользователя"""
    random_num = random.randint(10000, 99999)
    return {
        "email": f"test_user_{random_num}@yandex.ru",
        "password": "password123",
        "name": f"User_{random_num}"
    }


def create_user_via_api():
    """Создает пользователя через API и возвращает его данные вместе с токеном"""
    user_data = generate_user_data()
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code == 200:
        # В Stellar Burgers токен приходит в поле accessToken (уже с префиксом Bearer)
        user_data["token"] = response.json().get("accessToken")
    return user_data


def delete_user_via_api(token):
    """Удаляет пользователя по токену"""
    headers = {"Authorization": token}
    requests.delete(f"{BASE_URL}/auth/user", headers=headers)


def create_order_via_api(token):
    """
    Создает заказ через API и возвращает ответ сервера.
    Ответ содержит поле 'order' с номером заказа.
    """
    headers = {"Authorization": token}
    payload = {"ingredients": INGREDIENTS}
    
    response = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)
    return response.json()