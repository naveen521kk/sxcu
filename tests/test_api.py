import json
import os
import time

import pytest

pathFile = os.path.dirname(os.path.abspath(__file__))
img_loc = os.path.join(pathFile, "assets", "sharex.png")


def test_ogproperties() -> None:
    from sxcu import SXCU, og_properties

    og = og_properties(
        color="#000", title="Some title", description="A cool description!"
    )
    con = json.dumps(
        {
            "color": "#000",
            "title": "Some title",
            "description": "A cool description!",
        }
    )
    assert con == og.export()
    t = SXCU()
    a = t.upload_image(file=img_loc, og_properties=og)

    assert a is not None


def test_upload_keys_default_domain() -> None:
    from sxcu import SXCU

    t = SXCU()
    con = t.upload_image(file=img_loc)
    expected_keys = ["url", "del_url", "thumb"]
    assert (
        list(con.keys()).sort() == expected_keys.sort()
    )  # sorting because keys are arraged different


@pytest.mark.xfail(run=False, reason="sxcu optimises images")
def test_upload_image_default_domain() -> None:
    import requests

    from sxcu import SXCU

    t = SXCU()
    con = t.upload_image(file=img_loc, noembed=True)

    con = requests.get(con["url"])
    assert open(img_loc, "rb") == con.content


# TODO: Test subdomains


def test_delete_image() -> None:

    from sxcu import SXCU

    time.sleep(60)  # to prevent overloading server
    t = SXCU()
    con = t.upload_image(file=img_loc, noembed=True)
    a = SXCU.delete_image(con["del_url"])
    assert a is True


def test_image_info() -> None:
    from sxcu import SXCU

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


def test_sxcu_file_parser() -> None:
    from sxcu import SXCU

    sxcu_file = os.path.join(pathFile, "assets", "sxcu.net - python.is-ne.at.sxcu")
    time.sleep(60)
    t = SXCU(file_sxcu=sxcu_file)
    con = t.upload_image(file=img_loc, noembed=True)

    # test domain
    assert con["url"].startswith("https://python.is-ne.at")

    # test keys
    expected_keys = ["url", "del_url", "thumb"]
    assert list(con.keys()).sort() == expected_keys.sort()


def test_sxcu_file_parser_no_argument() -> None:
    from sxcu import SXCU

    sxcu_file = os.path.join(pathFile, "assets", "sxcu.net - why-am-i-he.re.sxcu")
    time.sleep(60)
    t = SXCU(file_sxcu=sxcu_file)
    con = t.upload_image(file=img_loc, noembed=True)

    # test domain
    assert con["url"].startswith("https://why-am-i-he.re")

    # test keys
    expected_keys = ["url", "del_url", "thumb"]
    assert list(con.keys()).sort() == expected_keys.sort()


def test_upload_test() -> None:
    time.sleep(60)
    import requests

    from sxcu import SXCU

    b = SXCU.upload_text("Hello, from sxcu Python Library. Test.")
    con = requests.get(b["url"])

    assert con.status_code == 200


def test_list_subdomains() -> None:
    time.sleep(60)
    from sxcu import SXCU

    b = SXCU.domain_list(1)
    req_keys = ["domain", "upload_count", "public", "img_views"]

    assert list(b[0].keys()).sort() == req_keys.sort()


def test_list_subdomains_all() -> None:
    time.sleep(60)
    from sxcu import SXCU

    b = SXCU.domain_list(-1)
    req_keys = ["domain", "upload_count", "public", "img_views"]

    assert list(b[0].keys()).sort() == req_keys.sort()


def test_upload_text() -> None:
    time.sleep(60)

    import requests

    from sxcu import SXCU

    con = SXCU.upload_text("Testing From Python Library")

    c = requests.get(con["url"])
    assert c.status_code == 200


def test_create_link() -> None:
    time.sleep(60)

    import requests

    from sxcu import SXCU

    t = SXCU()
    con = t.create_link("https://github.com/naveen521kk/sxcu")

    c = requests.get(con["url"])
    assert c.status_code == 200
