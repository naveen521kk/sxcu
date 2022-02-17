import os
import time
import pytest

from sxcu import SXCU

collection_details = []
pathFile = os.path.dirname(os.path.abspath(__file__))
img_loc = os.path.join(pathFile, "assets", "sharex.png")

@pytest.mark.slow
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

@pytest.mark.slow
def test_upload_image_to_collection() -> None:
    time.sleep(60)
    t = SXCU()
    con = t.upload_file(
        file=img_loc,
        collection=collection_details["collection_id"],
        collection_token=collection_details["collection_token"],
        noembed=True,
    )

    assert con["url"].startswith("https://sxcu.net")
