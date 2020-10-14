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
