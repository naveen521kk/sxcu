"""

    constants.py
    ~~~~~~~~~~~~

    Some useful constants which contains status code
    and helps in error handling.

"""
__all__ = []
from enum import Enum

from .__version__ import __version__

SXCU_SUCCESS_CODE = 200


class DefaultDomains(Enum):
    """DefaultDomains A Emum representing all the default API
    URL's to use.
    """

    UPLOAD_TEXT = "https://cancer-co.de/upload"
    API_ENDPOINT = "https://sxcu.net/api/"


HEADERS = {"User-Agent": f"PySXCU/{__version__} (https://pypi.org/project/sxcu/)"}
# see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent#syntax
