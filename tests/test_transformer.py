import pandas as pd
from src.transformer import transform_data


def test_transform_single_record():
    df = pd.DataFrame([{
        "customer_id": 1,
        "customer_name": "Acme",
        "plan": "Pro",
        "price": 49.0,
        "usage": 100,
    }])
    records = transform_data(df)
    assert len(records) == 1
    assert records[0]["customer_id"] == 1
    assert records[0]["customer_name"] == "Acme"
    assert records[0]["subscription"]["plan"] == "Pro"
    assert records[0]["subscription"]["price"] == 49.0
    assert records[0]["usage"] == 100


def test_transform_handles_nan_name():
    df = pd.DataFrame([{
        "customer_id": 2,
        "customer_name": None,
        "plan": "Basic",
        "price": 19.0,
        "usage": 50,
    }])
    records = transform_data(df)
    assert records[0]["customer_name"] == "Unknown Customer"


def test_transform_multiple_records():
    df = pd.DataFrame([
        {"customer_id": 1, "customer_name": "A", "plan": "Pro", "price": 49, "usage": 100},
        {"customer_id": 2, "customer_name": "B", "plan": "Basic", "price": 19, "usage": 200},
    ])
    records = transform_data(df)
    assert len(records) == 2
    assert records[0]["customer_id"] == 1
    assert records[1]["customer_id"] == 2
