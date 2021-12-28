import pytest
from sxcu import SXCU, OGProperties
import json
from .test_api import IMG_LOC


@pytest.mark.slow
def test_ogproperties() -> None:

    og = OGProperties(
        color="#000", title="Some title", description="A cool description!"
    )
    con = json.dumps(
        {
            "color": "#000",
            "title": "Some title",
            "description": "A cool description!",
            "discord_hide_url": False,
        }
    )
    assert con == og.export()
    t = SXCU()
    a = t.upload_file(file=IMG_LOC, og_properties=og)

    assert a is not None


def test_import_og_properties() -> None:
    og = OGProperties(
        color="#000", title="Some title", description="A cool description!"
    )
    exp = og.export()
    con = OGProperties.from_json(exp)
    assert con.export() == og.export()