import pandas as pd
from src.validator import validate_data, filter_valid_records


def _make_df(rows):
    return pd.DataFrame(rows, columns=["customer_id", "customer_name", "plan", "price", "usage"])


def test_valid_data_returns_no_errors():
    df = _make_df([[1, "Acme", "Pro", 49, 100]])
    errors, invalid = validate_data(df)
    assert errors == []
    assert invalid == set()


def test_missing_name_detected():
    df = _make_df([[1, None, "Pro", 49, 100]])
    errors, invalid = validate_data(df)
    assert any("Missing customer names" in e for e in errors)
    assert 0 in invalid


def test_negative_usage_detected():
    df = _make_df([[1, "Acme", "Pro", 49, -50]])
    errors, invalid = validate_data(df)
    assert any("Negative usage" in e for e in errors)
    assert 0 in invalid


def test_duplicate_ids_detected():
    df = _make_df([
        [1, "Acme", "Pro", 49, 100],
        [1, "Acme Copy", "Basic", 19, 200],
    ])
    errors, invalid = validate_data(df)
    assert any("Duplicate" in e for e in errors)
    assert 1 in invalid  # second occurrence is rejected


def test_filter_valid_records():
    df = _make_df([
        [1, "Acme", "Pro", 49, 100],
        [2, None, "Basic", 19, 50],
        [3, "Gamma", "Pro", 49, -10],
    ])
    _, invalid = validate_data(df)
    valid_df, rejected_df = filter_valid_records(df, invalid)
    assert len(valid_df) == 1
    assert valid_df.iloc[0]["customer_id"] == 1
    assert len(rejected_df) == 2
