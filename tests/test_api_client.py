from unittest.mock import patch, MagicMock
from src.api_client import upload_record, upload_batch


@patch("src.api_client.requests.post")
def test_upload_success(mock_post):
    mock_post.return_value = MagicMock(status_code=200)
    result = upload_record(
        {"customer_id": 1}, api_url="http://test.com", retries=1
    )
    assert result is True


@patch("src.api_client.requests.post")
def test_upload_failure(mock_post):
    mock_post.return_value = MagicMock(status_code=500)
    result = upload_record(
        {"customer_id": 1}, api_url="http://test.com", retries=1, backoff_factor=0
    )
    assert result is False


@patch("src.api_client.requests.post")
def test_upload_retry_then_success(mock_post):
    fail = MagicMock(status_code=500)
    success = MagicMock(status_code=200)
    mock_post.side_effect = [fail, success]
    result = upload_record(
        {"customer_id": 1}, api_url="http://test.com", retries=2, backoff_factor=0
    )
    assert result is True
    assert mock_post.call_count == 2


@patch("src.api_client.upload_record")
def test_upload_batch(mock_upload):
    mock_upload.side_effect = [True, False, True]
    records = [
        {"customer_id": 1},
        {"customer_id": 2},
        {"customer_id": 3},
    ]
    results = upload_batch(records, api_url="http://test.com")
    assert results["success"] == [1, 3]
    assert results["failed"] == [2]
