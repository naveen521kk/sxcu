from sxcu._utils import join_url

def test_join_url():
    assert join_url('https://foo.com', '/files') == 'https://foo.com/files'
    assert join_url('https://foo.com/','/files') == 'https://foo.com/files'
    assert join_url('https://foo.com/','files') == 'https://foo.com/files'
