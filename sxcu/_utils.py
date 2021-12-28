"""


    utils.py
    ~~~~~~~~
    Extra utils used internally.
"""
__all__ = []
from .__logger__ import logger
from .constants import SXCU_SUCCESS_CODE
from .exceptions import SXCUError


def join_url(subdomain: str, path: str) -> str:
    if path[0] != "/":
        path = "/" + path
    if subdomain[-1] != "/":
        return subdomain + path
    return subdomain[:-1] + path


def raise_error(status_code: int, error_code: int, error: str) -> None:
    logger.error(
        "The status_code from remote is %s which was expected to be %s.",
        status_code,
        SXCU_SUCCESS_CODE,
    )
    logger.error("The error code is: %s ", error_code)
    logger.error("The reason for this error is: %s", error)
    raise SXCUError(error)


def get_id_from_url(url: str) -> str:
    """Get the id of the image from the url.
    The url is of the format https://sxcu.net/{image_id},
    so we simply split the url by `/` and return the last part.

    Parameters
    ----------
    url : str
        The original url.

    Returns
    -------
    str
        The id of the image.
    """
    sp = url.split("/")
    return sp[-1]
