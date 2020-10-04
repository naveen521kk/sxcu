from os import R_OK, access
from pathlib import Path
from typing import Optional

import pyperclip
import typer
from pydantic import BaseModel, HttpUrl, ValidationError
from rich.console import Console
from rich.table import Table

from .sxcu import SXCU

allowed_file_types = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".bmp",
    ".tif",
    ".tiff",
    ".webm",
]
app = typer.Typer()
ERROR_COLOR = "RED"
IMAGE_FORMAT_NOT_SUPPORTED_MESSAGE = "Image format is not supported"
IMAGE_NOT_READABLE_MESSAGE = "Image file isn't readable."
SUCESS_MESSAGE_COLOR = "YELLOW UNDERLINE"
console = Console()


class ParseUrl(BaseModel):
    url: HttpUrl


@app.callback(help="CLI for accessing sxcu.net api.")
def callback() -> None:
    """
    This is just empty. Later this would be used.
    """


@app.command()
def upload(
    image: Path = typer.Argument(..., help="The image path reletive or absolute"),
    noembed: Optional[bool] = typer.Option(False, help="dedicated page or direct URL"),
    collection: Optional[str] = typer.Argument(
        None,
        help="The collection ID to which you want to upload to if you want to upload to a collection",
    ),
    collection_token: Optional[str] = typer.Argument(
        None,
        help="The collection upload token if one is required by the collection you're uploading to.",
    ),
) -> None:
    """
    Upload an Image to https://sxcu.net
    """
    image_absolute_path = image.absolute()
    if not image.is_file():
        typer.secho("Image file doesn't exists", fg=ERROR_COLOR)
        raise typer.Exit(code=1)
    if image.is_dir():
        typer.secho("Directory Upload is not implemented", fg=ERROR_COLOR)
        raise NotImplementedError
    if not access(image, R_OK):
        typer.secho(IMAGE_NOT_READABLE_MESSAGE, fg=ERROR_COLOR)
        raise typer.Exit(code=1)
    if image.suffix in allowed_file_types:
        handler = SXCU()
        result = handler.upload_image(
            image_absolute_path,
            noembed=noembed,
            collection=collection,
            collection_token=collection_token,
        )
        pyperclip.copy(result["url"])
        table = Table(title="Image Details")
        table.add_column("Details", justify="center", style="green")
        table.add_column("URL", justify="center", style="cyan")
        table.add_row("Upload URL", result["url"])
        table.add_row("Delete URL", result["del_url"])
        table.add_row("Thumb URL", result["thumb"])
        console.print(table)
        console.print(
            "Url has been Copied to Clipboard",
            style=SUCESS_MESSAGE_COLOR,
            justify="center",
        )
    else:
        error_message = typer.style(IMAGE_FORMAT_NOT_SUPPORTED_MESSAGE, fg=ERROR_COLOR)
        typer.echo(error_message)
        raise typer.Exit(code=1)


@app.command()
def createlink(
    link: str = typer.Argument(..., help="The link to which you want to redirect.")
) -> None:
    """
    Create a shorten link.
    """
    try:
        link = ParseUrl(url=link).url
    except ValidationError:
        console.print("Not a Valid URL", style=ERROR_COLOR)
        console.print_exception()
    handler = SXCU()
    content = handler.create_link(link)
    table = Table(title="Link Details")
    table.add_column("Details", justify="center", style="green")
    table.add_column("URL", justify="center", style="cyan")
    table.add_row("The shortened link is", content["url"])
    table.add_row("Delete URL", content["del_url"])
    console.print(table)
    pyperclip.copy(content["url"])
    console.print(
        "Url has been Copied to Clipboard",
        style=SUCESS_MESSAGE_COLOR,
        justify="center",
    )
