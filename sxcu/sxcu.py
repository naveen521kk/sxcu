"""Python API wrapper for sxcu.net
"""
import json
import typing as T
import warnings

from .__client__ import RequestClient
from .__logger__ import logger
from ._utils import join_url, raise_error
from .constants import (
    SXCU_SUCCESS_CODE,
    DefaultDomains,
    status_code_general,
    status_code_upload_text,
    status_code_upload_file
)
from .exceptions import SXCUError
from .og_properties import OGProperties

__all__ = ["SXCU"]

request_handler = RequestClient()


class SXCU:
    """The Main class for sxcu.net request"""

    def __init__(
        self, subdomain: str = None, upload_token: str = None, file_sxcu: str = None
    ) -> None:
        """This initialise the handler

        Parameters
        ==========
        subdomain : :class:`str`, optional
            The subdomain you get from sxcu.net
        upload_token : :class:`str`, optional
            The upload token that comes along with subdomain
        file_sxcu : :class:`str`,optional
            The sxcu file you have got. Parses only ``RequestURL`` and ``upload_token``.

            .. note ::

                The content in ``.sxcu`` file has more priority than passed parameters.
        """
        self.subdomain = subdomain if subdomain else "https://sxcu.net"
        self.upload_token = upload_token  # Don't log upload_token
        self.file_sxcu = file_sxcu
        self.api_endpoint = DefaultDomains.API_ENDPOINT.value
        if file_sxcu:
            with open(file_sxcu) as sxcu_file:
                con = json.load(sxcu_file)
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
        warnings.warn(
            "SXCU.upload_image() is deprecated. " "Use SXCU.upload_file() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.upload_file(*args, **kwargs)

    def upload_file(
        self,
        file: str,
        collection: T.Optional[str] = None,
        collection_token: T.Optional[str] = None,
        noembed: T.Optional[bool] = False,
        og_properties: T.Optional[OGProperties] = None,
        self_destruct: bool = False,
    ) -> T.Union[dict, list]:
        """This uploads image to sxcu

        Parameters
        ==========
        file:
            The path of File to Upload
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
        url = join_url(self._get_api_endpoint(default_domain=False), "/files/create")
        with open(file, "rb") as img_file:
            files = {"file": img_file}
            res = request_handler.post(url, files=files, data=data)
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
    def edit_collection(
        collection_id: str,
        collection_token: str,
        title: T.Optional[str] = None,
        desc: T.Optional[str] = None,
        unlisted: bool = False,
        regen_token: bool = False,
        empty_collection: bool = False,
        delete_collection: bool = False,
    ) -> dict:
        """Edit an existing collection.

        Parameters
        ==========
        collection_id:
            The ID of the collection to be edited.
        collection_token:
            The current token of that collection.
        title:
            The new title of the collection.
        desc:
            The new description of the collection.
        unlisted:
            If ``True`` the collection will be made unlisted.
        regen_token:
            If ``True``, it will generate a new token for the collection
            and return it in the response.
        empty_collection:
            If ``True`` it will disassociate all of the images
            in the collection from it.
        delete_collection:
            If ``True`` it  will disassociate all of the
            images in the collection from it and delete the collection.

        Returns
        =======
        :class:`dict`
            The returned JSON from the request.
        """
        data: T.Dict[str, T.Union[str, bool]] = {
            "action": "edit_collection",
            "collection_token": collection_token,
        }
        if title:
            data["title"] = title
        if desc:
            data["desc"] = desc
        if unlisted:
            data["unlisted"] = unlisted
        if regen_token:
            data["regen_token"] = ""
        if empty_collection:
            data["empty_collection"] = ""
        if delete_collection:
            data["delete_collection"] = ""
        url = DefaultDomains.EDIT_COLLECTIONS.value.format(collection_id=collection_id)
        res = request_handler.post(url, data=data)
        if res.status_code != SXCU_SUCCESS_CODE:
            error_response = res.json()
            raise_error(
                res.status_code, error_response["code"], error_response["error"]
            )
        final = res.json()
        if isinstance(final, list):
            final = dict()
            final["token"] = None
        return final

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
        data = {
            "action": "create_collection",
            "title": title,
            "private": private,
            "unlisted": unlisted,
        }
        if desc:
            data["desc"] = desc
        res = request_handler.post(
            DefaultDomains.API_ENDPOINT.value,
            data=data,
        )
        if str(res.status_code) in status_code_general:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is %s",
                status_code_general[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_general[str(res.status_code)]["desc"])
        return res.json()

    @staticmethod
    def collection_details(collection_id: str) -> T.Union[dict, list]:
        """Get collection details and list of images (if any are uploaded)
        for a given collection

        Parameters
        ==========
        collection_id : :class:`str`
            collection_id returned when creating a collection.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        res = request_handler.get(
            DefaultDomains.COLLECTION_DETAILS.value.format(collection_id=collection_id),
        )
        if str(res.status_code) in status_code_general:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is %s",
                status_code_general[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_general[str(res.status_code)]["desc"])
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
        if str(res.status_code) in status_code_upload_text:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is %s",
                status_code_upload_file[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_upload_text[str(res.status_code)]["desc"])
        return res.json()

    @staticmethod
    def file_meta(image_id: str = None, image_url: str = None) -> T.Union[dict, list]:
        """Get basic details about an image on sxcu.net or any of its subdomain

        Parameters
        ==========
        image_id : :class:`str`
            The id of the image. For example, if ``https://sxcu.net/QNeo92`` is the
            image URL then ``QNeo92`` will be the ``image_id``.

            .. note ::

                The ``image_id`` can be from any subdomain also
                as alway the id would be same.

        imageUrl : :class:`str`
            The image URL returned of sucessful upload.
            For example, ``https://sxcu.net/QNeo92``.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
        """
        if image_url is None and image_id is None:
            raise AttributeError("Either one of image_id or image_url is necessary")
        if image_url is None:
            image_url = DefaultDomains.IMAGE_DETAILS.value.format(image_id=image_id)
        if image_url[-5:-1] != ".json":
            image_url += ".json"
        res = request_handler.get(image_url)
        if str(res.status_code) in status_code_general:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is %s",
                status_code_general[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_general[str(res.status_code)]["desc"])
        return res.json()

    @staticmethod
    def domain_list(count: int = -1) -> list:
        """This lists all the public domains available, sorted by upload count.

        Parameters
        ==========
        count : :class:`int`, optional
            Number of domains to return. If count=``-1`` it lists all.

        .. warning::

            The returned list contains bytes. Using :py:func:`str.encode`. Please use
            :py:func:`bytes.decode` for decoding it.

        Returns
        =======
        :class:`list`
            The returned JSON from the request.
        """
        res = request_handler.get(DefaultDomains.DOMAINS_LIST.value)
        if str(res.status_code) in status_code_general:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is %s",
                status_code_general[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_general[str(res.status_code)]["desc"])
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
