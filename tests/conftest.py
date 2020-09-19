import scxu.sxcu as SXCU
import scxu.sxcu as SXCU

def test_res():
    a = SXCU.SXCU()
    b = SXCU.og_properties("#000", "Some title", "A cool description!")
    c = a.upload_image(r"D:\sample.png", og_properties=b, noembed=False)
    print(c)
    assert a==b
    print(SXCU.SXCU.domain_list(5))
