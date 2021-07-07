import os
from inspect import getfullargspec

import pytest
import requests

from sxcu import SXCU
from sxcu.constants import (
    status_code_create_link,
    status_code_general,
    status_code_upload_image,
    status_code_upload_text,
)
from sxcu.exceptions import SXCUError

handler = SXCU()
pathFile = os.path.dirname(os.path.abspath(__file__))
img_loc = os.path.join(pathFile, "assets", "sharex.png")


class MockResponse:
    def __init__(self, status_code) -> None:
        self._status_code = status_code

    @property
    def text(self):
        return {"mock_key": "mock_response"}

    @property
    def headers(self):
        return {}

    @property
    def status_code(self):
        return self._status_code


@pytest.mark.parametrize("status_code", [int(i) for i in status_code_upload_image])
def test_upload_image_status_code(monkeypatch, status_code):
    def mock_get(*args, **kwargs):
        return MockResponse(status_code)

    monkeypatch.setattr(requests, "post", mock_get)

    with pytest.raises(SXCUError) as exc_info:
        handler.upload_image(file=img_loc)
    assert str(exc_info.value) == status_code_upload_image[str(status_code)]["desc"]


@pytest.mark.parametrize("status_code", [int(i) for i in status_code_create_link])
def test_create_link_status_code(monkeypatch, status_code):
    def mock_post(*args, **kwargs):
        return MockResponse(status_code)

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_post)

    with pytest.raises(SXCUError) as exc_info:
        handler.create_link("https://example.com")
    assert str(exc_info.value) == status_code_create_link[str(status_code)]["desc"]


@pytest.mark.parametrize(
    "status_code,test_function",
    [
        (int(i), j)
        for i in status_code_general
        for j in [
            handler.edit_collection,
            handler.create_collection,
            handler.collection_details,
            handler.domain_list
        ]
    ],
)
def test_status_code_general(monkeypatch, status_code, test_function):
    def mock_post(*args, **kwargs):
        return MockResponse(status_code)

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_post)
    dummy_args = ["test"] * 10
    with pytest.raises(SXCUError) as exc_info:
        _inspect = getfullargspec(test_function)
        args = (
            len(_inspect.args) - len(_inspect.defaults)
            if _inspect.defaults is not None
            else len(_inspect.args)
        )
        test_function(*dummy_args[:args])
    assert str(exc_info.value) == status_code_general[str(status_code)]["desc"]


@pytest.mark.parametrize(
    "status_code",
    [int(i) for i in status_code_general],
)
def test_image_details(monkeypatch, status_code):
    def mock_post(*args, **kwargs):
        return MockResponse(status_code)

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_post)

    with pytest.raises(SXCUError) as exc_info:
        handler.image_details(image_id="test")
    assert str(exc_info.value) == status_code_general[str(status_code)]["desc"]


@pytest.mark.parametrize("status_code", [int(i) for i in status_code_upload_text])
def test_upload_text_status_code(monkeypatch, status_code):
    def mock_post(*args, **kwargs):
        return MockResponse(status_code)

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setattr(requests, "get", mock_post)

    with pytest.raises(SXCUError) as exc_info:
        handler.upload_text("https://example.com")
    assert str(exc_info.value) == status_code_upload_text[str(status_code)]["desc"]
