"""

    __client__.py
    ~~~~~~~~~~~~~

    This module wraps aroud ``Requests`` for logging
    and checking purpose.
"""
import requests  # pylint: disable=import-error

from .__logger__ import logger
from .constants import HEADERS

__all__ = ["RequestClient"]


class RequestClient:
    """:class:`RequestClient` is internally used to communicated with
    ``Requests`` Library.
    """

    def __init__(self, headers: dict = None) -> None:
        """This initaite the handlers.
        Parameters
        ==========
        headers : :class:`dict`, optional
            The extra header needed to be added to the Request.

        """
        if headers and isinstance(headers, dict):
            self.headers = headers
        else:
            self.headers = HEADERS
        logger.debug("Headers recieved are: %s", self.headers)

    def post(
        self, url: str, headers: dict = None, **kwargs  # noqa ANN003
    ) -> requests.models.Response:
        """Pass all the parameter to :func:`requests.post`.
        Also, adding the neccessary headers. Also, the newly passed header
        would overide the default.
        Parameters
        ==========
        headers : :class:`str`, optional
            The header needed to be added to the Request.

            .. important ::

                    The header would overide the default header.

        """
        logger.debug("Trying to do a Post Requests to %s", url)
        headers = self.headers if headers is None else headers
        con = requests.post(url, headers=headers, **kwargs)
        logger.debug("Recieved Headers from %s: %s", url, con.headers)
        logger.debug("status_code returned was:%s", con.status_code)
        response = con.text
        logger.info("Recieved Response: %s", response)
        return con

    def get(
        self, url: str, headers: dict = None, **kwargs  # noqa ANN003
    ) -> requests.models.Response:
        """Pass all the parameter to :func:`requests.get`.
        Also, adding the neccessary headers. Also, the newly passed header
        would overide the default.
        Parameters
        ==========
        headers : :class:`str`, optional
            The header needed to be added to the Request.

            .. important ::

                    The header would overide the default header.

        """
        logger.debug("Trying to do Get Requests to %s", url)
        headers = self.headers if headers is None else headers
        con = requests.get(url=url, headers=headers, **kwargs)
        logger.debug("Recieved Headers from %s: %s", url, con.headers)
        # Don't use json instead implement a custom class here?
        response = con.text
        logger.info("Recieved Response: %s", response)
        return con
