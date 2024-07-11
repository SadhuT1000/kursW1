from unittest.mock import patch
import pytest
from src.views import views
import json


expected = {
    "greeting": "Доброе утро!",
    "cards": {"cards_info": 1234},
    "top_transactions": {"transactions": 1234},
    "currency_rates": {"USD": 90},
    "stock_prices": {"APPL": 1500},
}
expected_json = json.dumps(expected, ensure_ascii=False)


@patch("src.views.stock_rates")
@patch("src.views.currency_rates")
@patch("src.views.json_loader")
@patch("src.views.top_five_transactions")
@patch("src.views.card_info")
@patch("src.views.reading_excel")
def test_views(
    mock_views_reading_excel,
    mock_views_card_info,
    mock_views_top_five_transactions,
    mock_json_loader,
    mock_views_currency_rates,
    mock_views_stock_rates,
):
    mock_views_reading_excel.return_value = {"some_card": 1234}
    mock_views_card_info.return_value = {"cards_info": 1234}
    mock_views_top_five_transactions.return_value = {"transactions": 1234}
    mock_json_loader.return_value = ["USD", "EUR"]
    mock_views_currency_rates.return_value = {"USD": 90}
    mock_views_stock_rates.return_value = {"APPL": 1500}
    assert views("2024-07-06 10:42:30") == expected_json


def test_views_with_wrong_date():
    with pytest.raises(Exception) as exc_info:
        views("ABC")
        assert str(exc_info.value) == "При работе функции произошла ошибка!"
