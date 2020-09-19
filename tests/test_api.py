import json

def test_ogproperties():
    from sxcu import og_properties
    og = og_properties(color="#000", title="Some title", description="A cool description!")
    con= json.dumps({
                "color": "#000",
                "title": "Some title",
                "description": "A cool description!",
            })
    assert con==og.export()

def test_upload_keys_default_domain():
    from sxcu import SXCU
    img_loc="tests/assets/glen-ardi-ljXFGnvmlno-unsplash.jpg"
    t=SXCU()
    con=t.upload_image(file=img_loc)
    expected_keys=["url","del_url","thumb"]
    assert list(con.keys()).sort()==expected_keys.sort() #sorting because keys are arraged different
def test_upload_image_default_domain():
    from sxcu import SXCU
    import requests
    img_loc="tests/assets/yoonjae-baik-F8ZR9BmWD3E-unsplash.jpg"
    t=SXCU()
    con=t.upload_image(file=img_loc,noembed=True)
    con=requests.get(con["url"])
    assert open("img_loc","rb")==con.content




    

