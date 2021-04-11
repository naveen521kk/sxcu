"""Python API wrapper for sxcu.net
"""
import json
from typing import Dict, Union

from .__client__ import RequestClient
from .__logger__ import logger
from .constants import (
    status_code_create_link,
    status_code_general,
    status_code_upload_image,
    status_code_upload_text,
)
from .exceptions import SXCUError

__all__ = ["OGProperties", "SXCU"]

request_handler = RequestClient()


class OGProperties:
    """
    This is a helper class for main SXCU function. This helps you to reuse
    the :class:`OGProperties`.
    """

    def __init__(
        self,
        color: str = None,
        description: str = None,
        title: str = None,
        discord_hide_url: bool = False,
    ) -> None:
        self.color = color
        self.description = description
        self.title = title
        self.discord_hide_url = discord_hide_url

    def export(self) -> str:
        """Exports the Property set to a JSON file.

        Returns
        =======
        :class:`str`
            Using ``json.dumps`` the content of JSON file is dumped.
        """
        return json.dumps(
            {
                "color": self.color,
                "title": self.title,
                "description": self.description,
                "discord_hide_url": self.discord_hide_url,
            }
        )

    @classmethod
    def from_json(cls, contents: str) -> "OGProperties":
        """Import the Property set from parsing JSON.

        Parameters
        ==========
        contents: :class:`str`
            The contents in JSON which needs to be parsed.

        Returns
        =======
        :class:`str`
            Using ``json.dumps`` the content of JSON file is dumped.
        """
        _dict = json.loads(contents)

        color = _dict["color"]
        description = _dict["description"]
        title = _dict["title"]
        discord_hide_url = _dict["discord_hide_url"]
        return cls(color, description, title, discord_hide_url)


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

                The content in ``.scxu`` file has more priority than passed parameters.
        """
        self.subdomain = subdomain if subdomain else "https://sxcu.net"
        self.upload_token = upload_token  # Not logging upload_token
        self.file_sxcu = file_sxcu
        self.api_endpoint = "https://sxcu.net/api"
        if file_sxcu:
            with open(file_sxcu) as sxcu_file:
                con = json.load(sxcu_file)
            # requests url already contain `/upload` removing that.
            self.subdomain = "/".join(con["RequestURL"].split("/")[:-1])
            if "Arguments" in con:
                self.upload_token = con["Arguments"]["token"]
        logger.debug("subdomain: %s", self.subdomain)

    def upload_image(
        self,
        file: str,
        collection: str = None,
        collection_token: str = None,
        noembed: bool = False,
        og_properties: OGProperties = None,
    ) -> Union[dict, list]:
        """This uploads image to sxcu

        Parameters
        ==========
        file : :class:`str`, optional
            The path of File to Upload
        collection : :class:`str`, optional
            The collection ID to which you want to upload to if
            you want to upload to a collection
        collection_token : :class:`str`, optional
            The collection upload token if one is required by the
            collection you're uploading to.
        noembed : :class:`bool`, optional
            If ``True``, the uploader will return a direct URL to the
            uploaded image, instead of a dedicated page.
        og_properties : :class:`OGProperties`, optional
            This will configure the OpenGraph properties of the file's page, effectively
            changing the way it embeds in various websites and apps.

        Returns
        =======
        :class:`dict` or :class:`list`
            The returned JSON from the request.
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
        url = (
            self.subdomain + "upload"
            if self.subdomain[-1] == "/"
            else self.subdomain + "/upload"
        )
        with open(file, "rb") as img_file:
            files = {"image": img_file}
            res = request_handler.post(url, files=files, data=data)
        if str(res.status_code) in status_code_upload_image:
            logger.error(
                "The status_code was %s which was expected to be 200.", res.status_code
            )
            logger.error(
                "The reason for this error is: %s",
                status_code_upload_image[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_upload_image[str(res.status_code)]["desc"])
        # Don't use json instead implement a custom class here.
        return res.json()

    def create_link(self, link: str) -> Union[dict, list]:
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
        url = (
            self.subdomain + "shorten"
            if self.subdomain[-1] == "/"
            else self.subdomain + "/shorten"
        )
        res = request_handler.post(url, data={"link": link})
        if str(res.status_code) in status_code_create_link:
            logger.error(
                "The status_code was %s which was expected to be 200.", res.status_code
            )
            logger.error(
                "The reason for this error is: %s",
                status_code_create_link[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_create_link[str(res.status_code)]["desc"])
        return res.json()

    @staticmethod
    def edit_collection(
        collection_id: str,
        collection_token: str,
        title: str = None,
        desc: str = None,
        unlisted: bool = False,
        regen_token: bool = False,
        empty_collection: bool = False,
        delete_collection: bool = False,
    ) -> dict:
        """Edit an existing collection.

        Parameters
        ==========
        collection_id : :class:`str`
            The ID of the collection to be edited.
        collection_token : :class:`str`
            The current token of that collection.
        title : :class:`str`, optional
            The new title of the collection.
        desc : :class:`str`, optional
            The new description of the collection.
        unlisted : :class:`bool`, optional
            If ``True`` the collection will be made unlisted.
        regen_token : :class:`bool`, optional
            If ``True``, it will generate a new token for the collection
            and return it in the response.
        empty_collection : :class:`bool`, optional
            If ``True`` it will disassociate all of the images
            in the collection from it.
        delete_collection : :class:`bool`, optional
            If ``True`` it  will disassociate all of the
            images in the collection from it and delete the collection.

        Returns
        =======
        :class:`dict`
            The returned JSON from the request.
        """
        data: Dict[str, Union[str, bool]] = {
            "action": "edit_collection",
            "collection_id": collection_id,
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
        res = request_handler.post("https://sxcu.net/api/", data=data)
        if str(res.status_code) in status_code_general:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is: %s",
                status_code_general[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_general[str(res.status_code)]["desc"])
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
        desc: str = None,
    ) -> Union[dict, list]:
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
        res = request_handler.post("https://sxcu.net/api/", data=data)
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
    def collection_details(collection_id: str) -> Union[dict, list]:
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
        res = request_handler.get(f"https://sxcu.net/c/{collection_id}.json")
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
    def upload_text(text: str) -> Union[dict, list]:
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
        res = request_handler.post("https://cancer-co.de/upload", data={"text": text})
        if str(res.status_code) in status_code_upload_text:
            logger.error(
                "The status_code was %s which was expected to be 200.",
                res.status_code,
            )
            logger.error(
                "The reason for this error is %s",
                status_code_upload_image[str(res.status_code)]["desc"],
            )
            raise SXCUError(status_code_upload_text[str(res.status_code)]["desc"])
        return res.json()

    @staticmethod
    def image_details(image_id: str = None, image_url: str = None) -> Union[dict, list]:
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
            image_url = f"https://sxcu.net/{image_id}.json"
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
        res = request_handler.get("https://sxcu.net/api?action=domains")
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
