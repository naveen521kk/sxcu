"""Python API wrapper for sxcu.net subdomains
"""
import requests
import json

# token=d6208525-a58a-4b91-8dc3-bcb7ad086445
# dom=pls.click-if-you-da.re

__all__=["og_properties","SXCU"]
class og_properties(object):
    def __init__(self, color=None, description=None, title=None):
        self.color = color
        self.description = description
        self.title = title

    def export(self):
        return json.dumps(
            {
                "color": self.color,
                "title": self.title,
                "description": self.description,
            }
        )


class SXCU:
    """The Main class for sxcu.net request"""

    def __init__(
        self, subdomain: str = None, upload_token: str = None, file_sxcu: str = None
    ):
        """This initialise the class

        Parameters
        ==========
        subdomain : :class:`str`, optional
            The subdomain you get from sxcu.net
        upload_token : :class:`str`, optional
            The upload token that comes along with subdomain
        file_sxcu : :class:`str`,optional
            The sxcu file you have got. Parses only ``RequestURL``.
        """
        self.subdomain = subdomain if subdomain else "https://sxcu.net"
        self.upload_token = upload_token
        self.file_sxcu = file_sxcu
        if file_sxcu:
            with open(file_sxcu) as f:
                con = json.load(f)
            self.subdomain = con["RequestURL"]

    def upload_image(
        self,
        file: str,
        collection: str = None,
        collection_token: str = None,
        noembed: bool = False,
        og_properties: og_properties = None,
    ):
        """This uploads image to sxcu

        Parameters
        ==========
        file : :class:`str`, optional
            The path of File to Upload
        collection : :class:`str`, optional
            The collection ID to which you want to upload to if you want to upload to a collection
        collection_token : :class:`str`, optional
            The collection upload token if one is required by the collection you're uploading to.
        noembed : :class:`bool`, optional
            If ``True``, the uploader will return a direct URL to the uploaded image, instead of a dedicated page.
        og_properties : :class:`og_properties`, optional
            This will configure the OpenGraph properties of the file's page, effectively changing the way it embeds in various websites and apps.

        Returns
        =======
        :class:`dict`
            The returned JSON from the request.
        """
        files = {"image": open(file, "rb")}
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
        res = requests.post(url=url, files=files, data=data)
        return res.json()

    def create_collection(
        self,
        title: str,
        private: bool = False,
        unlisted: bool = False,
        desc: str = None,
    ):
        """Create a new collection on sxcu.net.
        Note:If you are creating one time / bot collections you must make them unlisted!

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
        :class:`dict`
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
        con = requests.post("https://sxcu.net/api/", data=data)
        return con.json()

    def collection_details(self, CollectionId: str):
        """Get collection details and list of images (if any are uploaded) for a given collection

        Parameters
        ==========
        CollectionId : :class:`str`
            CollectionId returned when creating a collection.

        Returns
        =======
        :class:`dict`
            The returned JSON from the request.
        """
        con = requests.get(f"https://sxcu.net/c/{CollectionId}.json")
        return con.json()

    def create_link(self, link: str):
        """Creates a new link.

        Parameters
        ==========
        link : :class:`str`
            The link to which you want to redirect.

        Returns
        =======
        :class:`dict`
            The returned JSON from the request.
        """
        con = requests.post(self.subdomain, data={"link": link})
        return con.json()

    def upload_text(self, text: str):
        """Uploads an text to sxcu.net (via cancer-co.de)

        Parameters
        ==========
        text : :class:`str`
            The text being uploaded.

        Returns
        =======
        :class:`dict`
            The returned JSON from the request.
        """
        con = requests.post("https://cancer-co.de/upload", data={"text": text})
        return con.json()

    @staticmethod
    def domain_list(count: int = -1):
        # todo
        """This lists all the public domains available, sorted by upload count.

        Parameters
        ==========
        count : :class:`int`, optional
            Number of domains to return. If count=``-1`` it lists all.

        Returns
        =======
        :class:`list`
            The returned JSON from the request.
        """
        con = requests.get("https://sxcu.net/api?action=domains")
        conJson = con.text
        with open("d.txt", "wb") as f:
            f.write(con.content)
        return con.json()

        if count == -1:
            return con.json()
        else:
            return con.json()
