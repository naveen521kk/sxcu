import json
import os
import time

import pytest


def test_ogproperties() -> None:
    from sxcu import og_properties

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


def test_upload_keys_default_domain() -> None:
    from sxcu import SXCU

    pathFile = os.path.dirname(os.path.abspath(__file__))
    img_loc = os.path.join(pathFile, "assets", "glen-ardi-ljXFGnvmlno-unsplash.jpg")
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

    pathFile = os.path.dirname(os.path.abspath(__file__))
    img_loc = os.path.join(pathFile, "assets", "yoonjae-baik-F8ZR9BmWD3E-unsplash.jpg")

    t = SXCU()
    con = t.upload_image(file=img_loc, noembed=True)

    con = requests.get(con["url"])
    assert open(img_loc, "rb") == con.content


# TODO: Test subdomains


def test_delete_image() -> None:

    from sxcu import SXCU

    pathFile = os.path.dirname(os.path.abspath(__file__))
    img_loc = os.path.join(pathFile, "assets", "yoonjae-baik-F8ZR9BmWD3E-unsplash.jpg")
    time.sleep(30)  # to prevent overloading server
    t = SXCU()
    con = t.upload_image(file=img_loc, noembed=True)
    a = SXCU.delete_image(con["del_url"])
    assert a is True


def test_image_info() -> None:
    from sxcu import SXCU

    pathFile = os.path.dirname(os.path.abspath(__file__))
    img_loc = os.path.join(pathFile, "assets", "yoonjae-baik-F8ZR9BmWD3E-unsplash.jpg")
    # upload image first
    t = SXCU()
    con = t.upload_image(file=img_loc, noembed=True)

    details = SXCU.image_details(image_url=con["url"])

    assert con["url"] == details["url"]
    # Now try using id
    id_url = con["url"].split("/")[-1].split(".")[0]
    details_id = SXCU.image_details(image_id=id_url)

    assert details_id["url"] == con["url"]

    try:
        SXCU.image_details()
        assert False
    except AttributeError:
        assert True
