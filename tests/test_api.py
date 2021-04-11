
import os
import time

import pytest
import requests

from sxcu import SXCU

pathFile = os.path.dirname(os.path.abspath(__file__))
img_loc = os.path.join(pathFile, "assets", "sharex.png")



@pytest.mark.slow
def test_upload_keys_default_domain_and_delete_image() -> None:
    time.sleep(60)

    t = SXCU()
    con = t.upload_image(file=img_loc)
    expected_keys = ["url", "del_url", "thumb"]
    assert (
        list(con.keys()).sort() == expected_keys.sort()
    )  # sorting because keys are arraged different

    a = SXCU.delete_image(con["del_url"])
    assert a is True

@pytest.mark.slow
@pytest.mark.xfail(run=False, reason="sxcu optimises images")
def test_upload_image_default_domain() -> None:
    t = SXCU()
    con = t.upload_image(file=img_loc, noembed=True)

    con = requests.get(con["url"])
    assert open(img_loc, "rb") == con.content


# TODO: Test subdomains

@pytest.mark.slow
def test_image_info() -> None:

    # upload image first
    t = SXCU()
    time.sleep(60)
    con = t.upload_image(file=img_loc, noembed=True)
    details = SXCU.image_details(image_url=con["url"])

    assert con["url"] == details["url"]
    # Now try using id
    time.sleep(60)
    id_url = con["url"].split("/")[-1].split(".")[0]
    details_id = SXCU.image_details(image_id=id_url)

    assert details_id["url"] == con["url"]

    try:
        SXCU.image_details()
        assert False
    except AttributeError:
        assert True

@pytest.mark.slow
def test_sxcu_file_parser() -> None:

    sxcu_file = os.path.join(pathFile, "assets", "sxcu.net - python.is-ne.at.sxcu")
    time.sleep(60)
    t = SXCU(file_sxcu=sxcu_file)
    con = t.upload_image(file=img_loc, noembed=True)

    # test domain
    assert con["url"].startswith("https://python.is-ne.at")

    # test keys
    expected_keys = ["url", "del_url", "thumb"]
    assert list(con.keys()).sort() == expected_keys.sort()

@pytest.mark.slow
def test_sxcu_file_parser_no_argument() -> None:

    sxcu_file = os.path.join(pathFile, "assets", "sxcu.net - why-am-i-he.re.sxcu")
    time.sleep(120)
    t = SXCU(file_sxcu=sxcu_file)
    con = t.upload_image(file=img_loc, noembed=True)

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
    t = SXCU()
    con = t.create_link("https://github.com/naveen521kk/sxcu")
    c = requests.get(con["url"])
    assert c.status_code == 200
