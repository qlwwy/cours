import json
from unittest.mock import patch

import pandas as pd

from src.services import load_operations_data, simple_search


@patch("pandas.read_excel")
def test_load_operations_data_success(mock_read_excel):
    mock_df = pd.DataFrame({"Дата операции": ["2024-01-01"], "Сумма": [100]})
    mock_read_excel.return_value = mock_df

    df = load_operations_data("fake_path.xlsx")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1


@patch("src.services.load_operations_data")
def test_simple_search_found(mock_load_data):
    test_data = pd.DataFrame(
        {
            "Дата операции": ["2024-01-01", "2024-01-02"],
            "Описание": ["Покупка кофе", "Покупка книг"],
        }
    )
    mock_load_data.return_value = test_data

    result_json = simple_search("кофе", "fake_path.xlsx")
    result = json.loads(result_json)

    assert "results_count" in result
    assert result["results_count"] == 1
    assert result["results"][0]["Описание"] == "Покупка кофе"


@patch("src.services.load_operations_data")
def test_simple_search_error(mock_load_data):
    mock_load_data.side_effect = Exception(
        "[Errno 2] No such file or directory: 'fake_path.xlsx'"
    )

    result_json = simple_search("что-то", "fake_path.xlsx")
    result = json.loads(result_json)

    assert "error" in result
    assert "[Errno 2] No such file or directory" in result["error"]
