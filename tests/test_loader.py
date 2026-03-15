import pytest
import pandas as pd
from src.loader import load_data


def test_load_data_success(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("customer_id,customer_name,plan,price,usage\n1,Test,Pro,49,100\n")
    df = load_data(str(csv_file))
    assert len(df) == 1
    assert list(df.columns) == ["customer_id", "customer_name", "plan", "price", "usage"]


def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError, match="Input file not found"):
        load_data("nonexistent.csv")


def test_load_data_missing_columns(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("customer_id,plan\n1,Pro\n")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_data(str(csv_file))


def test_load_data_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    with pytest.raises(ValueError, match="Input file is empty"):
        load_data(str(csv_file))
