import requests
import json
from config import TOKEN


class APIException(Exception):
    """Пользовательское исключение для ошибок API"""
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        """
        Получает цену валюты
        """
        base = base.upper()
        quote = quote.upper()

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество '{amount}'. Введите число.")

        if amount <= 0:
            raise APIException("Количество валюты должно быть больше 0")

        available_currencies = ['USD', 'EUR', 'RUB']

        if base not in available_currencies:
            raise APIException(
                f"Валюта '{base}' не поддерживается. Доступные валюты: {', '.join(available_currencies)}")

        if quote not in available_currencies:
            raise APIException(
                f"Валюта '{quote}' не поддерживается. Доступные валюты: {', '.join(available_currencies)}")

        if base == quote:
            raise APIException("Невозможно конвертировать одинаковые валюты")

        try:
            # Используем бесплатное API для курсов валют
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}')

            if response.status_code != 200:
                raise APIException("Ошибка при получении данных от сервера")

            data = json.loads(response.text)

            if quote not in data['rates']:
                raise APIException(f"Не удалось получить курс для валюты '{quote}'")

            rate = data['rates'][quote]
            result = amount * rate

            return round(result, 2)

        except requests.exceptions.ConnectionError:
            raise APIException("Ошибка соединения. Проверьте интернет-соединение.")
        except requests.exceptions.Timeout:
            raise APIException("Таймаут соединения.")
        except Exception as e:
            raise APIException(f"Произошла ошибка: {str(e)}")
