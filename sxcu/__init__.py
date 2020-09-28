"""
    SXCU
    ~~~~

    Python API wrapper for sxcu.net.

    :copyright: Copyright 2020 by Naveen M K
    :license: Apache-2.0 , see LICENSE for details.

"""
from .sxcu import SXCU, og_properties  # noqa F401

try:
    from importlib.metadata import version as importlib_metadata_version
except ImportError:
    from importlib_metadata import version as importlib_metadata_version

__version__ = importlib_metadata_version("sxcu")
