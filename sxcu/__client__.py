import requests

from .__logger__ import logger
from .constants import HEADERS

__all__ = ["RequestClient"]


class RequestClient:
    """``RequestClient`` is internally used to communicated with
    ``Requests`` Library.
    """

    def __init__(self, headers: dict = None) -> None:
        """This initaite the handlers.
        Parameters
        ==========
        headers : :class:`str`, optional
            The extra header needed to be added to the Request.
        """
        if headers and isinstance(headers, dict):
            self.headers = headers
        else:
            self.headers = HEADERS
        logger.DEBUG(f"Headers set as: {self.headers}")

    def post(
        self, url: str, headers: dict = None, **kwargs # noqa ANN003
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
        headers = self.headers if headers is None else headers
        con = requests.post(url, headers=headers, **kwargs)
        logger.DEBUG(f"Recieved Headers: {con.headers}")
        print(url)
        return con

    def get(self, url: str, headers: dict = None, **kwargs) -> requests.models.Response: # noqa ANN003
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
        headers = self.headers if headers is None else headers
        print(url)
        con = requests.get(url=url, headers=headers, **kwargs)
        return con
