import pytest
from src.utils import greetings, reading_excel, card_info, top_five_transactions
from unittest.mock import patch


@pytest.mark.parametrize(
    "date, expected", [("2024-07-06 14:42:30", "Добрый день!"), ("2044-12-06 04:42:30", "Доброй ночи!")]
)
def test_greetings(date, expected):
    assert greetings(date) == expected


def test_greetings_with_wrong_date():
    with pytest.raises(ValueError) as exc_info:
        greetings("abcd")
        assert str(exc_info.value) == "Введены некорректные данные!"


@patch("pandas.read_excel")
def test_reading_excel(mock_read_excel):
    mock_read_excel.return_value.to_dict.return_value = [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
        }
    ]
    result = reading_excel("test_file.xls")
    assert result == [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
        }
    ]


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
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
            ],
            [{"last_digits": "7197", "total_spent": -347.7, "cashback": -3.48}],
        )
    ],
)
def test_card_info(transactions, expected):
    assert card_info(transactions) == expected


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                {"Сумма операции": 1},
                {"Сумма операции": 9},
                {"Сумма операции": 4},
                {"Сумма операции": 31},
                {"Сумма операции": 11},
                {"Сумма операции": 17},
                {"Сумма операции": 100},
                {"Сумма операции": 5},
            ],
            [
                {"Сумма операции": 9},
                {"Сумма операции": 11},
                {"Сумма операции": 17},
                {"Сумма операции": 31},
                {"Сумма операции": 100},
            ],
        )
    ],
)
def test_top_five_transactions(transactions, expected):
    assert top_five_transactions(transactions) == expected
