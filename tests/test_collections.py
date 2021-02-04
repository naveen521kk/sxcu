import os
import time

from sxcu import SXCU

collection_details = []
pathFile = os.path.dirname(os.path.abspath(__file__))
img_loc = os.path.join(pathFile, "assets", "sharex.png")


def test_create_collections() -> None:
    time.sleep(120)
    global collection_details
    uploadInfo = {
        "title": "Python Test",
        "desc": "Testing from sxcu Python Library",
        "private": True,
    }
    a = SXCU.create_collection(unlisted=True, **uploadInfo)
    collection_details = a
    b = SXCU.collection_details(a["collection_id"])
    to_check = ["title", "desc"]
    for i in to_check:
        assert uploadInfo[i] == b[i]


def test_upload_image_to_collection() -> None:
    time.sleep(60)
    t = SXCU()
    con = t.upload_image(
        file=img_loc,
        collection=collection_details["collection_id"],
        collection_token=collection_details["collection_token"],
        noembed=True,
    )

    assert con["url"].startswith("https://sxcu.net")


def test_edit_collection_no_delete() -> None:
    time.sleep(120)
    from sxcu import SXCU

    con = SXCU.edit_collection(
        collection_id=collection_details["collection_id"],
        collection_token=collection_details["collection_token"],
        title="New Title",
        desc="Test Description",
        unlisted=True,
    )

    assert con["token"] is None


def test_edit_collection_regen_token() -> None:
    time.sleep(120)
    from sxcu import SXCU

    con = SXCU.edit_collection(
        collection_id=collection_details["collection_id"],
        collection_token=collection_details["collection_token"],
        regen_token=True,
    )

    assert con["token"] is not None
    collection_details["collection_token"] = con["token"]


def test_edit_collection_empty_collection() -> None:
    time.sleep(120)

    from sxcu import SXCU

    con = SXCU.edit_collection(
        collection_id=collection_details["collection_id"],
        collection_token=collection_details["collection_token"],
        empty_collection=True,
    )

    assert con["token"] is None


def test_edit_collection_delete_collection() -> None:
    time.sleep(120)

    from sxcu import SXCU

    con = SXCU.edit_collection(
        collection_id=collection_details["collection_id"],
        collection_token=collection_details["collection_token"],
        delete_collection=True,
    )

    assert con["token"] is None
