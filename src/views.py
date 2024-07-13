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


def views(date: str, transactions_df) -> str:
    """Функция принимает дату (строка) и DataFrame с данными по транзакциям.
    Возвращает ответ с приветствием, информацией по картам,
    топ-5 транзакций стоимость валюты и акций в виде json-строки."""
    try:
        logger.info("Функция начала свою работу.")
        transactions = transactions_df.to_dict(orient="records")
        logger.info("Функция собирает результаты работ своих подфункций.")
        greeting = greetings(date)
        logger.info("Функция приветствия завершила свою работу.")
        info_about_cards = card_info(transactions)
        logger.info("Функция по сбору информации по картам завершила свою работу.")
        five_transactions = top_five_transactions((transactions))
        logger.info("Функция топ-5 транзакций завершила свою работу.")
        users_settings = json_loader()
        currensy = currency_rates(users_settings[0])
        logger.info("Функция курса валют завершила свою работу.")
        stock = stock_rates(users_settings[1])
        logger.info("Функция котировок акций завершила свою работу.")
        logger.info("Функция формирует общий результат результат.")
        result_dict = {
            "greeting": greeting,
            "cards": info_about_cards,
            "top_transactions": five_transactions,
            "currency_rates": currensy,
            "stock_prices": stock,
        }
        result_json = json.dumps(result_dict, ensure_ascii=False)
        logger.info("Функция успешно завершила свою работу.")
        return result_json
    except Exception:
        logger.error("При работе функции произошла ошибка.")
        raise ValueError("При работе функции произошла ошибка.")


if __name__ == "__main__":
    transaction_info = reading_excel("operations.xls")
    print(views("2024-07-06 10:42:30", transaction_info))
