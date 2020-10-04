from os import R_OK, access
from pathlib import Path

import pyperclip
import typer
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
ERROR_COLOR = typer.colors.BRIGHT_RED
IMAGE_FORMAT_NOT_SUPPORTED_MESSAGE = "Image format is not supported"
IMAGE_NOT_READABLE_MESSAGE = "Image file isn't readable."
console = Console()


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
        pyperclip.copy(result["url"])
        table = Table(title="Image Details")
        table.add_column("Details", justify="center", style="green")
        table.add_column("URL", justify="center", style="cyan")
        table.add_row("Upload URL:", result["url"])
        table.add_row("Delete URL:", result["del_url"])
        table.add_row("Thumb URL", result["thumb"])
        console.print(table)
        console.print(
            "Url has been Copied to Clipboard",
            style="YELLOW UNDERLINE",
            justify="center",
        )
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
