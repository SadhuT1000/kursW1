import datetime
import os
from collections import defaultdict
from typing import Dict, List

import pandas as pd

from config import DATA_DIR


def greetings(date_string: str) -> str:
    """Функция принимает время в строке в формате '%Y-%m-%d %H:%M:%S',
    возвращает приветствие в зависимости от времени суток."""
    try:
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        time_for_greeting = date_object.time()
        greetings_dict = {
            "1": ("Доброе утро!", "05:00:01", "12:00:00"),
            "2": ("Добрый день!", "12:00:01", "17:00:00"),
            "3": ("Добрый вечер!", "17:00:01", "21:00:00"),
            "4": ("Доброй ночи!", "21:00:01", "00:00:00"),
            "5": ("Доброй ночи!", "00:00:01", "05:00:00"),
        }
        for greeting in greetings_dict:
            start, end = greetings_dict[greeting][1], greetings_dict[greeting][2]
            time_start = datetime.datetime.strptime(start, "%H:%M:%S").time()
            time_end = datetime.datetime.strptime(end, "%H:%M:%S").time()
            if time_start <= time_for_greeting <= time_end:
                return greetings_dict[greeting][0]
    except Exception:
        raise ValueError("Введены некорректные данные!")


def reading_excel(file_name: str) -> List[Dict]:
    """Функция принимает время в строке название файла excel,
    возвращает список транзакций(словарей) пригодный для дальнейшей обработки."""
    if file_name.endswith("xls") or file_name.endswith("xlsx"):
        file_with_dir = os.path.join(DATA_DIR, file_name)
        transactions_df = pd.read_excel(file_with_dir)
        result = transactions_df.to_dict(orient="records")
        return result
    else:
        raise ValueError("Неподдерживаемый формат файла!")


def card_info(transactions: List[Dict]) -> List[Dict]:
    """Функция принимает список транзакций(словарей).
    Возвращает список словарей с информацией по каждой карте: последние 4 цифры номера карты,
    общая сумма расходов, кэшбек (1 рубль на каждые 100 рублей)."""
    unique_card_nums = list(set([transaction["Номер карты"] for transaction in transactions]))
    expenditure_by_card = defaultdict(int)
    for card_num in unique_card_nums:
        for transaction in transactions:
            if transaction["Номер карты"] == card_num:
                expenditure_by_card[card_num] += transaction["Сумма операции"]
    result_transaction_list = []
    for item in expenditure_by_card:
        result_transaction_list.append(
            {
                "last_digits": item[1:],
                "total_spent": round(expenditure_by_card[item], 2),
                "cashback": round(expenditure_by_card[item] / 100, 2),
            }
        )
    return result_transaction_list


def top_five_transactions(transactions: List[Dict]) -> List[Dict]:
    """Функция принимает список транзакций(словарей).
    Возвращает список словарей с топ-пятью транзакциями по сумме операции."""
    sorted_transactions_list = sorted(transactions, key=lambda x: x["Сумма операции"])
    return sorted_transactions_list[-5:]


if __name__ == "__main__":
    print(greetings("2024-07-06 10:42:30"))
    data = reading_excel("operations.xls")
    print(card_info(data))
    print(
        card_info(
            [
                {
                    "Дата операции": "28.03.2018 09:24:15",
                    "Дата платежа": "29.03.2018",
                    "Номер карты": "*7197",
                    "Статус": "OK",
                    "Сумма операции": -150.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -150.0,
                    "Валюта платежа": "RUB",
                    "Кэшбэк": "nan",
                    "Категория": "Связь",
                    "MCC": 4814.0,
                    "Описание": "МТС",
                    "Бонусы (включая кэшбэк)": 3,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 150.0,
                },
                {
                    "Дата операции": "28.03.2018 08:23:56",
                    "Дата платежа": "30.03.2018",
                    "Номер карты": "*7197",
                    "Статус": "OK",
                    "Сумма операции": -197.7,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -197.7,
                    "Валюта платежа": "RUB",
                    "Кэшбэк": "nan",
                    "Категория": "Супермаркеты",
                    "MCC": 5411.0,
                    "Описание": "Billa",
                    "Бонусы (включая кэшбэк)": 3,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 197.7,
                },
            ]
        )
    )
    print(top_five_transactions(data))
    data_for_five = [
        {"Сумма операции": 1},
        {"Сумма операции": 9},
        {"Сумма операции": 4},
        {"Сумма операции": 31},
        {"Сумма операции": 11},
        {"Сумма операции": 17},
        {"Сумма операции": 100},
        {"Сумма операции": 5},
    ]
    print(top_five_transactions(data_for_five))
