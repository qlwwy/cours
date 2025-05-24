import pytest
import pandas as pd
from src.reports import spending_by_category

@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": ["01.10.2023 12:00:00", "02.10.2023 12:00:00", "03.10.2023 12:00:00"],
        "Сумма платежа": [100, 200, 300],
        "Категория": ["Супермаркеты", "Кафе", "Супермаркеты"],
        "Описание": ["Описание 1", "Описание 2", "Описание 3"],
        "Номер карты": ["1234", "5678", "9101"],
    }
    return pd.DataFrame(data)

def test_spending_by_category_empty_transactions():
    empty_transactions = pd.DataFrame()
    result = spending_by_category(empty_transactions, "Супермаркеты", "03.10.2023")
    assert result.empty

def test_spending_by_category_invalid_date_format(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты", "03-10-2023")
    assert result.empty

def test_spending_by_category_no_matching_category(sample_transactions):
    result = spending_by_category(sample_transactions, "Рестораны", "03.10.2023")
    assert result.empty

def test_spending_by_category_no_matching_date(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты", "01.09.2023")
    assert result.empty
