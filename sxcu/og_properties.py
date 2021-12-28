"""OGProperties declaration.
"""
__all__ = [
    "OGProperties",
]

import json
import typing as T


class OGProperties:
    """
    This is a helper class for main SXCU function. This helps you to reuse
    the :class:`OGProperties`.
    """

    def __init__(
        self,
        color: T.Union[str, bool] = None,
        description: T.Union[str, bool] = None,
        title: T.Union[str, bool] = None,
        discord_hide_url: bool = False,
        site_name: T.Union[str, bool] = None,
    ) -> None:
        self.color = color
        self.description = description
        self.title = title
        self.discord_hide_url = discord_hide_url
        self.site_name = site_name

    def export(self) -> str:
        """Exports the Property set to a JSON file.

        Returns
        =======
        :class:`str`
            Using ``json.dumps`` the content of JSON file is dumped.
        """
        return json.dumps(
            {
                "color": self.color or False,
                "title": self.title or False,
                "description": self.description or False,
                "discord_hide_url": self.discord_hide_url,
                "site_name": self.site_name or False,
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
        site_name = _dict["site_name"]
        return cls(color, description, title, discord_hide_url, site_name)
