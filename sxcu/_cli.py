"""Contains CLI code.
"""
import argparse
import logging
import sys
import tempfile
import typing
from pathlib import Path

import pyperclip
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.theme import Theme

from .exceptions import CLIError
from .sxcu import SXCU

custom_theme = Theme({"error": "bold red", "warning": "magenta", "code": "green"})
console = Console(theme=custom_theme)
SUCCESS_MESSAGE_COLOR = "YELLOW Underline"
FORMAT = "%(message)s"
logging.basicConfig(
    format=FORMAT,
    handlers=[
        RichHandler(
            level=logging.ERROR,
            console=console,
            show_time=False,
            show_path=False,
            show_level=False,
        )
    ],
)
logger = logging.getLogger("rich")

parser = argparse.ArgumentParser(prog="sxcu")

subparsers = parser.add_subparsers(title="subcommands")
parser.set_defaults(func=lambda *x: parser.print_help())  # print help by default


def handle_paste_subcommand(args: typing.Any) -> None:
    def print_result(result: typing.Dict[str, str]) -> None:
        pyperclip.copy(result["url"])
        table = Table(title="Upload Details")
        table.add_column("Details", justify="center", style="green")
        table.add_column("URL", justify="center", style="cyan")
        table.add_row("Upload URL", result["url"])
        table.add_row("Delete URL", result["del_url"])
        console.print(table)
        console.print(
            "Url has been Copied to Clipboard",
            style=SUCCESS_MESSAGE_COLOR,
            justify="center",
        )

    text = args.text or sys.stdin.read()
    sxcu_handler = SXCU()
    res = sxcu_handler.upload_text(text)
    print_result(res)


def paste_subcommand() -> None:
    paste = subparsers.add_parser(
        "paste",
        help="Uploads an text to sxcu.net",
    )
    paste.add_argument(
        "--text",
        type=str,
        help="The text to upload",
    )
    paste.set_defaults(func=handle_paste_subcommand, text="")


def handle_upload_command(args: typing.Any) -> None:
    def print_result(result: typing.Dict[str, str]) -> None:
        pyperclip.copy(result["url"])
        table = Table(title="Upload Details")
        table.add_column("Details", justify="center", style="green")
        table.add_column("URL", justify="center", style="cyan")
        table.add_row("Upload URL", result["url"])
        table.add_row("Delete URL", result["del_url"])
        table.add_row("Thumb URL", result["thumb"])
        console.print(table)
        console.print(
            "Url has been Copied to Clipboard",
            style=SUCCESS_MESSAGE_COLOR,
            justify="center",
        )

    if args.img_path and args.img:
        raise CLIError(
            "Received both [code]img_path[/code] and "
            "[code]img[/code]. Expected only one of them."
        )
    img = args.img
    sxcu_handler = SXCU()
    if not args.img_path:
        if img != "":
            img_data = img.encode()
        else:
            img_data = sys.stdin.buffer.read()
    else:
        img_data = Path(args.img_path).open("rb").read()
    with tempfile.TemporaryDirectory(prefix="sxcu") as tmpdir:
        tmpath = Path(tmpdir, "tmp.jpg")
        with tmpath.open("wb") as f:
            f.write(img_data)
        res = sxcu_handler.upload_file(tmpath)
        print_result(res)


def upload_subcommand() -> None:
    upload = subparsers.add_parser(
        "upload",
        help="Uploads an image or file to sxcu.net",
    )
    upload.add_argument(
        "--img-path",
        type=Path,
        help="Path to the image to upload",
        required=False,
    )
    upload.add_argument(
        "--img", type=str, help="Paste the image to upload", required=False
    )
    upload.set_defaults(func=handle_upload_command, img="")


def main() -> None:
    paste_subcommand()
    upload_subcommand()
    args = parser.parse_args()
    try:
        args.func(args)
    except CLIError as e:
        console.print(str(e), style="error")
        sys.exit(2)
