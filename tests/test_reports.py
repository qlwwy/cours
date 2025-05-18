import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.reports import get_expenses_by_day_of_week


def test_get_expenses_by_day_of_week_success():
    # Создаем мок для pd.read_excel
    df_mock = pd.DataFrame(
        {
            "date": [
                "2025-01-01",
                "2025-01-02",
                "2025-01-03",
                "2025-01-04",
                "2025-01-05",
            ],
            "amount": [100, 200, 150, 300, 250],
        }
    )

    with patch("pandas.read_excel", return_value=df_mock):
        result = get_expenses_by_day_of_week("fake_path.xlsx", "2025-01-01")
        result_dict = json.loads(result)

        assert isinstance(result_dict, list)
        assert len(result_dict) > 0


def test_get_expenses_by_day_of_week_empty_data():
    # Создаем мок для pd.read_excel с пустым DataFrame
    df_mock = pd.DataFrame({"date": [], "amount": []})

    with patch("pandas.read_excel", return_value=df_mock):
        result = get_expenses_by_day_of_week("fake_path.xlsx", "2025-01-01")
        result_dict = json.loads(result)

        assert result_dict["error"] == "Нет данных для выбранного периода."


def test_get_expenses_by_day_of_week_invalid_date_format():
    with patch(
        "pandas.read_excel",
        return_value=pd.DataFrame({"date": ["invalid_date"], "amount": [100]}),
    ):
        result = get_expenses_by_day_of_week("fake_path.xlsx", "invalid_date")
        result_dict = json.loads(result)

        assert "error" in result_dict


def test_get_expenses_by_day_of_week_file_not_found():
    with patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")):
        result = get_expenses_by_day_of_week("non_existent_file.xlsx", "2025-01-01")
        result_dict = json.loads(result)

        assert "error" in result_dict
