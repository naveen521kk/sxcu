# SXCU Python API Wrapper
<p align="center">
  <a href="https://pypi.org/project/sxcu/">
    <img src="https://img.shields.io/pypi/v/sxcu" alt="sxcu PyPI Version">
  </a>
  <a href="https://sxcu.syrusdark.website">
    <img src="https://readthedocs.org/projects/sxcu/badge/?version=latest" alt="sxcu Documentation Status">
  </a>
  <a href="https://opensource.org/licenses/Apache-2.0">
    <img src="https://img.shields.io/badge/License-Apache2.0-green.svg" alt"sxcu License">
  </a>
  <a href="https://codecov.io/gh/naveen521kk/sxcu">
    <img src="https://codecov.io/gh/naveen521kk/sxcu/branch/master/graph/badge.svg" alt="sxcu codecov">
  </a>
  <a href="https://lgtm.com/projects/g/naveen521kk/sxcu/alerts/">
    <img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/naveen521kk/sxcu.svg?logo=lgtm&logoWidth=18"/>
  </a>
  <a href="https://lgtm.com/projects/g/naveen521kk/sxcu/context:python">
    <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/naveen521kk/sxcu.svg?logo=lgtm&logoWidth=18"/>
  </a>
</p>

![sxcu-logo](https://github.com/naveen521kk/sxcu/raw/master/logo/readme-logo.png)
<p align="center">
A friendly API wrapper around https://sxcu.net.
</p>

## Installation

The package is published on
[PyPI](https://pypi.org/project/sxcu/) and can be installed by running:
```sh
pip install sxcu
```

## Basic Use

Easily query the sxcu.net from you Python code. The data returned from the sxcu.net
API is mapped to python resources:

```python
>>> import sxcu
>>> con = sxcu.SXCU()
>>> con.upload_image("foo.jpg")
{'url': 'https://sxcu.net/2kW7IT', 'del_url': 'https://sxcu.net/d/2kW7IT/455c7e40-9e3b-43fa-a95a-ac17dd920e55', 'thumb': 'https://sxcu.net/t/2kW7IT.jpeg'}
```
Ready for more? Look at our whole [documentation](https://sxcu.syrusdark.website/) on Read The Docs.

## Contributing
Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to
contribute to this project.

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://naveen.syrusdark.website"><img src="https://avatars1.githubusercontent.com/u/49693820?v=4" width="100px;" alt=""/><br /><sub><b>Naveen M K</b></sub></a><br /><a href="https://github.com/naveen521kk/sxcu/commits?author=naveen521kk" title="Code">💻</a> <a href="https://github.com/naveen521kk/sxcu/commits?author=naveen521kk" title="Documentation">📖</a> <a href="#maintenance-naveen521kk" title="Maintenance">🚧</a> <a href="#projectManagement-naveen521kk" title="Project Management">📆</a> <a href="https://github.com/naveen521kk/sxcu/pulls?q=is%3Apr+reviewed-by%3Anaveen521kk" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/naveen521kk/sxcu/commits?author=naveen521kk" title="Tests">⚠️</a> <a href="#platform-naveen521kk" title="Packaging/porting to new platform">📦</a></td>
    <td align="center"><a href="https://github.com/shahprog"><img src="https://avatars0.githubusercontent.com/u/40076722?v=4" width="100px;" alt=""/><br /><sub><b>shahprog</b></sub></a><br /><a href="https://github.com/naveen521kk/sxcu/issues?q=author%3Ashahprog" title="Bug reports">🐛</a> <a href="https://github.com/naveen521kk/sxcu/commits?author=shahprog" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
