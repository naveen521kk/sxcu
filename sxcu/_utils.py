"""


    utils.py
    ~~~~~~~~
    Extra utils used internally.
"""
__all__ = []
from .__logger__ import logger
from .constants import SXCU_SUCCESS_CODE
from .exceptions import SXCUError


def join_url(subdomain, path) -> str:
    if path[0] != "/":
        path = "/" + path
    if subdomain[-1] != "/":
        return subdomain + path
    return subdomain[:-1] + path


def raise_error(status_code, error_code, error):
    logger.error(
        "The status_code from remote is %s which was expected to be %s.",
        status_code,
        SXCU_SUCCESS_CODE,
    )
    logger.error("The error code is: %s ", error_code)
    logger.error("The reason for this error is: %s", error)
    raise SXCUError(error)
