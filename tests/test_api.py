import io
import json
import time
from pathlib import Path

import pytest
import requests

from sxcu import SXCU

FILE_PATH = Path(__file__).parent
IMG_LOC = Path(FILE_PATH, "assets", "sharex.png")
IMG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\x0cIDAT\x18Wc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82"


@pytest.mark.slow
def test_upload_keys_default_domain_and_delete_image() -> None:
    time.sleep(60)

    _t = SXCU()
    con = _t.upload_file(file=IMG_LOC)
    expected_keys = ["url", "del_url", "thumb"]
    assert (
        list(con.keys()).sort() == expected_keys.sort()
    )  # sorting because keys are arraged different

    _a = SXCU.delete_image(con["del_url"])
    assert _a is True


@pytest.mark.slow
@pytest.mark.xfail(run=False, reason="sxcu optimises images")
def test_upload_image_default_domain() -> None:
    t = SXCU()
    con = t.upload_file(file=IMG_LOC, noembed=True)

    con = requests.get(con["url"])
    assert open(IMG_LOC, "rb") == con.content


@pytest.mark.slow
def test_upload_with_io_bytes():
    _t = SXCU()
    con = _t.upload_file(io.BytesIO(IMG), noembed=True)
    file = requests.get(con["url"])
    assert IMG == file.content


# TODO: Test subdomains


@pytest.mark.slow
def test_image_info() -> None:

    # upload image first
    t = SXCU()
    time.sleep(60)
    con = t.upload_file(file=IMG_LOC, noembed=True)
    details = SXCU.file_details(image_url=con["url"])

    assert con["url"] == details["url"]
    # Now try using id
    time.sleep(60)
    id_url = con["url"].split("/")[-1].split(".")[0]
    details_id = SXCU.file_details(image_id=id_url)

    assert details_id["url"] == con["url"]

    try:
        SXCU.file_details()
        assert False
    except AttributeError:
        assert True


@pytest.mark.slow
def test_sxcu_file_parser() -> None:

    sxcu_file = Path(FILE_PATH, "assets", "sxcu.net - python.is-ne.at.sxcu")
    time.sleep(60)
    _t = SXCU(sxcu_config=sxcu_file)
    con = _t.upload_file(file=IMG_LOC, noembed=True)

    # test domain
    assert con["url"].startswith("https://python.is-ne.at")

    # test keys
    expected_keys = ["url", "del_url", "thumb"]
    assert list(con.keys()).sort() == expected_keys.sort()


@pytest.mark.slow
def test_sxcu_file_parser_no_argument() -> None:

    sxcu_file = Path(FILE_PATH, "assets", "sxcu.net - why-am-i-he.re.sxcu")
    time.sleep(120)
    t = SXCU(sxcu_config=sxcu_file)
    con = t.upload_file(file=IMG_LOC, noembed=True)

    # test domain
    assert con["url"].startswith("https://why-am-i-he.re")

    # test keys
    expected_keys = ["url", "del_url", "thumb"]
    assert list(con.keys()).sort() == expected_keys.sort()


@pytest.mark.slow
def test_upload_text() -> None:
    b = SXCU.upload_text("Hello, from sxcu Python Library. Test.")
    con = requests.get(b["url"])

    assert con.status_code == 200


@pytest.mark.slow
def test_list_subdomains() -> None:
    time.sleep(60)

    b = SXCU.domain_list(1)
    req_keys = ["domain", "upload_count", "public", "img_views"]

    assert list(b[0].keys()).sort() == req_keys.sort()


@pytest.mark.slow
def test_list_subdomains_all() -> None:
    b = SXCU.domain_list(-1)
    req_keys = ["domain", "upload_count", "public", "img_views"]

    assert list(b[0].keys()).sort() == req_keys.sort()


@pytest.mark.slow
def test_create_link() -> None:
    _t = SXCU()
    con = _t.create_link("https://github.com/naveen521kk/sxcu")
    _c = requests.get(con["url"])
    assert _c.status_code == 200


def test_sxcu_file_init():
    sxcu_file = Path(FILE_PATH, "assets", "sxcu.net - why-am-i-he.re.sxcu")
    _t = SXCU(sxcu_config=sxcu_file)
    assert _t.subdomain == "https://why-am-i-he.re"


def test_sxcu_file_init_with_token():
    sxcu_file = Path(FILE_PATH, "assets", "sxcu.net - python.is-ne.at.sxcu")
    _t = SXCU(sxcu_config=sxcu_file)
    assert _t.subdomain == "https://python.is-ne.at"
    assert _t.upload_token == "b8893b47-0e90-4fce-ad46-4264161a3a72"


class MockUploadResponse:
    def __init__(self, status_code, response) -> None:
        self._status_code = status_code
        self._response = response

    @property
    def text(self):
        return self._response

    @property
    def headers(self):
        return {}

    @property
    def status_code(self):
        return self._status_code

    def json(self):
        return json.loads(self._response)


def test_upload_mock(monkeypatch):
    response = json.dumps(
        {
            "url": "https://sxcu.net/53BhgPNB1",
            "del_url": "https://sxcu.net/d/53BhgPNB1/81388fb6-8d20-4c8e-b256-f5472c88e062",
            "thumb": "https://sxcu.net/t/53BhgPNB1.png",
        }
    )

    def mock_get(*args, **kwargs):
        assert "token" in kwargs["data"]
        assert kwargs["data"]["token"] == "b8893b47-0e90-4fce-ad46-4264161a3a72"
        return MockUploadResponse(200, response)

    monkeypatch.setattr(requests, "post", mock_get)

    sxcu_file = Path(FILE_PATH, "assets", "sxcu.net - python.is-ne.at.sxcu")
    _t = SXCU(sxcu_config=sxcu_file)
    a = _t.upload_file(IMG_LOC)
    assert json.dumps(a) == response
