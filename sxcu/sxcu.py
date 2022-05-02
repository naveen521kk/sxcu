"""Python API wrapper for sxcu.net
"""
import io
import json
import typing as T
import warnings

from .__client__ import RequestClient
from .__logger__ import logger
from ._utils import get_id_from_url, join_url, raise_error
from .constants import SXCU_SUCCESS_CODE, DefaultDomains
from .og_properties import OGProperties

__all__ = ["SXCU"]

request_handler = RequestClient()


class SXCU:
    """The Main class for sxcu.net request"""

    def __init__(
        self,
        subdomain: str = None,
        upload_token: str = None,
        sxcu_config: T.Union[str, dict, io.StringIO] = None,
        *,
        file_sxcu: str = None,
    ) -> None:
        """This initialise the handler

        Parameters
        ==========
        subdomain : :class:`str`, optional
            The subdomain you get from sxcu.net
        upload_token : :class:`str`, optional
            The upload token that comes along with subdomain
        sxcu_config : :class:`str`,optional
            The sxcu configuration you have. Parses only ``RequestURL`` and ``upload_token``.

            .. note ::

                The content in ``.sxcu`` file has more priority than passed parameters.
        file_sxcu : :class:`str`, optional
            File location to sxcu configuration. Kept for backwards compatibility.

        """
        self.subdomain = subdomain if subdomain else "https://sxcu.net"
        self.upload_token = upload_token  # Don't log upload_token
        self.file_sxcu = sxcu_config
        self.api_endpoint = DefaultDomains.API_ENDPOINT.value
        if file_sxcu:
            warnings.warn(
                "file_sxcu parameter is deprecated. " "Use sxcu_config instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            sxcu_config = file_sxcu

        if sxcu_config:
            if isinstance(sxcu_config, io.StringIO):
                con = json.load(sxcu_config)
            elif isinstance(sxcu_config, dict):
                con = sxcu_config
            else:
                with open(sxcu_config) as sxcu_file:
                    con = json.load(sxcu_file)
            self.sxcu_config = con
            # requests url already contain `/api/files/create` remove that.
            self.subdomain = "/".join(con["RequestURL"].split("/")[:-3])
            if "Arguments" in con:
                self.upload_token = con["Arguments"]["token"]
        logger.debug("subdomain: %s", self.subdomain)

    def _get_api_endpoint(self, default_domain: bool = False) -> str:
        return (
            join_url("https://sxcu.net", "/api")
            if default_domain
            else join_url(self.subdomain, "/api")
        )

    def upload_image(self, *args: T.Any, **kwargs: T.Any) -> T.Union[dict, list]:
        """This method is deprecated.
        Use :meth:`~.SXCU.upload_file` instead.
        """
        warnings.warn(
            "SXCU.upload_image() is deprecated. " "Use SXCU.upload_file() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.upload_file(*args, **kwargs)

    def upload_file(
        self,
        name: str = None,
        fileobj: io.BytesIO = None,
        collection: T.Optional[str] = None,
        collection_token: T.Optional[str] = None,
        noembed: T.Optional[bool] = False,
        og_properties: T.Optional[OGProperties] = None,
        self_destruct: bool = False,
        *,
        file: str = None,
    ) -> T.Union[dict, list]:
        """This uploads image to sxcu

        Parameters
        ==========
        name:
            The pathname of file to upload.
        file:
            aliased to name, for backwards compatibility.
        fileobj:
            If fileobj is given, it is used for reading the file.
        collection:
            The collection ID to which you want to upload to if
            you want to upload to a collection
        collection_token:
            The collection upload token if one is required by the
            collection you're uploading to.
        noembed:
            If ``True``, the uploader will return a direct URL to the
            uploaded image, instead of a dedicated page.
        og_properties:
            This will configure the OpenGraph properties of the file's page, effectively
            changing the way it embeds in various websites and apps.
        self_destruct:
            If ``True``, the file will be deleted automatically after
            24 hours.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.

        Raises
        ======
        :class:`~.SXCUError`:
            Any error from the request side.
        """
        data = {}
        if self.upload_token:
            data["token"] = self.upload_token
        if collection:
            data["collection"] = collection
        if collection_token:
            data["collection_token"] = collection_token
        if noembed:
            data["noembed"] = ""
        if og_properties:
            data["og_properties"] = og_properties.export()
        if self_destruct:
            data["self_destruct"] = ""
        if file:
            name = file
        url = join_url(self._get_api_endpoint(default_domain=False), "/files/create")
        _file_opened = False
        try:
            if fileobj is None:
                fileobj = open(name, "rb")
                _file_opened = True
            res = request_handler.post(url, files={"file": fileobj}, data=data)
        finally:
            if _file_opened:
                fileobj.close()
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        # Don't use json instead implement a custom class here.
        return res.json()

    def create_link(self, link: str) -> T.Union[dict, list]:
        """Creates a new link.

        Parameters
        ==========
        link : :class:`str`
            The link to which you want to redirect.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        url = join_url(self._get_api_endpoint(), "/links/create")
        res = request_handler.post(url, data={"link": link})
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        return res.json()

    @staticmethod
    def create_collection(
        title: str,
        private: bool = False,
        unlisted: bool = False,
        desc: T.Optional[str] = None,
    ) -> T.Union[dict, list]:
        """Create a new collection on sxcu.net.

        .. note::

            If you are creating one time / bot collections you must make them unlisted!

        Parameters
        ==========
        title : :class:`str`
            The title of the collection.
        private : :class:`bool`, optional
            Whether the collection should be private or not.
        unlisted : :class:`bool`, optional
            Whether the collection should be unlisted or not.
        desc : :class:`str`, optional
            The description of the collection.
        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        url = join_url(DefaultDomains.API_ENDPOINT.value, "/collections/create")
        data = {
            "title": title,
            "private": private,
            "unlisted": unlisted,
        }
        if desc:
            data["desc"] = desc
        res = request_handler.post(
            url,
            data=data,
        )
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        return res.json()

    @staticmethod
    def collection_details(*args: T.Any, **kwargs: T.Any) -> T.Union[dict, list]:
        """This method is deprecated.
        Use :meth:`~.SXCU.collection_meta` instead.
        """
        warnings.warn(
            "SXCU.collection_details() is deprecated. "
            "Use SXCU.collection_meta() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return SXCU.collection_meta(*args, **kwargs)

    @staticmethod
    def collection_meta(collection_id: str) -> T.Union[dict, list]:
        """Get collection details and list of images (if any are uploaded)
        for a given collection.

        Parameters
        ==========
        collection_id : :class:`str`
            collection_id returned when creating a collection.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        url = join_url(
            DefaultDomains.API_ENDPOINT.value, f"/collections/{collection_id}"
        )
        res = request_handler.get(
            url,
        )
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )

        return res.json()

    @staticmethod
    def upload_text(text: str) -> T.Union[dict, list]:
        """Uploads an text to sxcu.net (via cancer-co.de)

        Parameters
        ==========
        text : :class:`str`
            The text being uploaded.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        res = request_handler.post(
            DefaultDomains.UPLOAD_TEXT.value,
            data={"text": text},
        )
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        return res.json()

    @staticmethod
    def image_details(*args: T.Any, **kwargs: T.Any) -> T.Union[dict, list]:
        """This method is deprecated.

        Use :meth:`~.SXCU.file_meta` instead.
        """
        warnings.warn(
            "SXCU.image_details() is deprecated. " "Use SXCU.file_meta() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return SXCU.file_meta(*args, **kwargs)

    @staticmethod
    def file_meta(
        file_id: str = None,
        file_url: str = None,
        image_id: str = None,
        image_url: str = None,
    ) -> T.Union[dict, list]:
        """Get basic details about an image on sxcu.net or any of its subdomain

        Parameters
        ==========
        file_id : :class:`str`
            The id of the image. For example, if ``https://sxcu.net/QNeo92`` is the
            image URL then ``QNeo92`` will be the ``image_id``.

            .. note ::

                The ``image_id`` can be from any subdomain also
                as alway the id would be same.

        file_url : :class:`str`
            The image URL returned of successfully upload.
            For example, ``https://sxcu.net/QNeo92``.
            Either one of :param:`file_id` or :param:`file_url`
            is required.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        if image_url is not None:
            warnings.warn(
                "The parameter 'image_url' is deprecated. " "Use 'file_url' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            if file_url is None:
                file_url = image_url
        if image_id is not None:
            warnings.warn(
                "The parameter 'image_id' is deprecated. " "Use 'file_id' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            if file_id is None:
                file_id = image_id

        if file_id is None:
            if file_url is None:
                raise AttributeError("Either one of file_id or file_url is necessary")
            else:
                file_id = get_id_from_url(image_url)
        url = join_url(DefaultDomains.API_ENDPOINT.value, f"/files/{file_id}")
        res = request_handler.get(url)
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        return res.json()

    @staticmethod
    def domain_list(*args: T.Any, **kwargs: T.Any) -> T.Union[dict, list]:
        """This method is deprecated.

        Use :meth:`~.SXCU.list_subdomain` instead.
        """
        warnings.warn(
            "SXCU.domain_list() is deprecated. " "Use SXCU.list_subdomain() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return SXCU.list_subdomain(*args, **kwargs)

    @staticmethod
    def list_subdomain(count: int = -1) -> list:
        """This lists all the public domains available, sorted by upload count.

        Parameters
        ==========
        count : :class:`int`, optional
            Number of domains to return. If count=``-1`` it lists all.

        .. warning::

            The returned list contains bytes encoded using :py:func:`str.encode`.
            Please use :py:func:`bytes.decode` for decoding it.

        Returns
        =======
        :class:`list`
            The returned JSON from the request.
        """
        url = join_url(DefaultDomains.API_ENDPOINT.value, "/subdomains")
        res = request_handler.get(url)
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        if count == -1:
            to_encode = res.json()
        else:
            to_encode = res.json()[:count]
        for i in enumerate(to_encode):
            temp = {}
            for j in i[1]:
                if isinstance(i[1][j], str):
                    temp[j] = i[1][j].encode()
            to_encode[i[0]] = temp
        return to_encode

    @staticmethod
    def delete_image(delete_url: str) -> bool:
        """Deletes images from sxcu.net

        Parameters
        ==========
        delete_url : :class:`str`
            The delete URL returned from sxcu.net while uploading.
        Returns
        =======
        :class:`bool`
            Deleted or not
        """
        con = request_handler.get(delete_url)
        return bool(con.status_code == 200)
