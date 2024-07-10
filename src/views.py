import json
import logging


from config import VIEWS_LOGS
from src.utils import (
    card_info,
    currency_rates,
    greetings,
    json_loader,
    reading_excel,
    stock_rates,
    top_five_transactions,
)

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(VIEWS_LOGS, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def views(date: str) -> str:
    """Функция принимает дату (строка). Возвращает ответ с приветствием,
    информацией по картам, топ-5 транзакций стоимость валюты и акций в виде json-строки."""
    logger.info("Функция начала свою работу.")
    logger.info("Функция собирает результаты работ своих подфункций.")
    greeting = greetings(date)
    transaction_info = reading_excel("operations.xls")
    info_about_cards = card_info(transaction_info)
    five_transactions = top_five_transactions((transaction_info))
    users_settings = json_loader()
    currensy = currency_rates(users_settings[0])
    stock = stock_rates(users_settings[1])
    logger.info("Функция формирует общий результат результат.")
    result_dict = {
        "greeting": greeting,
        "cards": info_about_cards,
        "top_transactions": five_transactions,
        "currency_rates": currensy,
        "stock_prices": stock,
    }
    result_json = json.dumps(result_dict, ensure_ascii=False, indent=2)
    logger.info("Функция успешно завершила свою работу.")
    return result_json


if __name__ == "__main__":
    print(views("2024-07-06 10:42:30"))
