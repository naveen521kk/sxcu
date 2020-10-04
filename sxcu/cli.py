from os import R_OK, access
from pathlib import Path

import pyperclip
import typer

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
ERROR_COLOR = typer.colors.BRIGHT_RED
IMAGE_FORMAT_NOT_SUPPORTED_MESSAGE = "Image format is not supported"
IMAGE_NOT_READABLE_MESSAGE = "Image file isn't readable."


@app.callback(help="CLI for accessing sxcu.net api.")
def callback() -> None:
    """
    This is just empty. Later this would be used.
    """


@app.command()
def upload(image: Path) -> None:
    """
    Upload an Image to https://sxcu.net
    """
    image_absolute_path = image.absolute()
    typer.echo(image_absolute_path)
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
        result = handler.upload_image(image_absolute_path)
        a = typer.style("Image Url:", fg=typer.colors.GREEN, bold=True)
        b = typer.style(result["url"], fg=typer.colors.YELLOW, bold=True)
        pyperclip.copy(result["url"])
        typer.echo(a)
        typer.echo(b)
    else:
        error_message = typer.style(IMAGE_FORMAT_NOT_SUPPORTED_MESSAGE, fg=ERROR_COLOR)
        typer.echo(error_message)
        raise typer.Exit(code=1)


'''
@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")
'''
