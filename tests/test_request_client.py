import requests

from sxcu.__client__ import RequestClient


class MockResponse:
    @property
    def text(self):
        return {"mock_key": "mock_response"}
    @property
    def headers(self):
        return {}

def test_headers(monkeypatch) -> None:
    headers = {"User-Agent": "python-sxcu"}
    def mock_get(*args, **kwargs):
        assert args is not None
        assert 'headers' in kwargs
        assert kwargs['headers'] == headers
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)
    client=RequestClient(headers=headers)
    client.get("https://dummy_url")
