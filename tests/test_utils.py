import pytest
import pandas as pd
from unittest.mock import patch

from src.utils import load_operations_data


@patch('pandas.read_excel')
def test_load_operations_data_success(mock_read_excel):
    mock_df = pd.DataFrame({
        "Дата операции": ["2024-01-01", "2024-01-02"]
    })
    mock_read_excel.return_value = mock_df

    result = load_operations_data("fake_path.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert "Дата операции" in result.columns


@patch('pandas.read_excel')
def test_load_operations_data_missing_column(mock_read_excel):
    mock_df = pd.DataFrame({
        "Другое поле": ["2024-01-01"]
    })
    mock_read_excel.return_value = mock_df

    with pytest.raises(ValueError, match="Ожидаемая колонка 'Дата операции' отсутствует"):
        load_operations_data("fake_path.xlsx")