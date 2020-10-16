"""

    constants.py
    ~~~~~~~~~~~~

    Some useful constants which contains status code
    and helps in error handling.

"""
from .__version__ import __version__

status_code_upload_image = {
    "403": {
        "message": "Invalid upload token",
        "desc": "The specified upload token does not match the domain's upload token.",
    },
    "404": {
        "message": "Collection not found",
        "desc": "The specified collection was not found.",
    },
    "405": {
        "message": "Request is not POST",
        "desc": "The request method must be POST.",
    },
    "406": {
        "message": "Upload error 101x",
        "desc": "An error occurred while handling the uploaded file.",
    },
    "407": {
        "message": "Subdomain is private, a valid upload token is required",
        "desc": "The sub domain you tried to upload to is private, and requires a valid upload token in order to upload to it.",
    },
    "409": {
        "message": "No file sent",
        "desc": "No binary file was sent in the 'image' field.",
    },
    "410": {
        "message": "Collection is private but no collection token provided",
        "desc": "The collection you tried to upload to is set to private and requires a collection token in order to upload to it.",
    },
    "412": {
        "message": "User-agent header not set",
        "desc": "The request did not contain a User-Agent header.",
    },
    "413": {
        "message": "File is over the size limit",
        "desc": "Uploaded file is larger than 95 MB.",
    },
    "415": {
        "message": "File type not allowed.",
        "desc": "The type of the uploaded file is not supported.",
    },
    "416": {
        "message": "Invalid collection token",
        "desc": "The specified collection token does not match the collection's token.",
    },
    "422": {
        "message": "Malformed JSON in OpenGraph properties",
        "desc": "The OpenGraph properties JSON array could not be properly parsed, and is most likely malformed.",
    },
    "429": {"message": None, "desc": "The request exceeded the rate limit."},
    "500": {
        "message": "The file was not uploaded due to an unknown error",
        "desc": "An unknown error has occurred while processing the file, try again later.",
    },
}
status_code_upload_text = {
    "409": {
        "message": None,
        "desc": "The text POST param is missing.",
    },
    "413": {
        "message": None,
        "desc": "Text is too long (8 MB).",
    },
    "429": {"message": None, "desc": "The request exceeded the rate limit."},
}
status_code_create_link = {
    "400": {
        "message": None,
        "desc": "The text POST param is missing or invalid URL",
    },
    "429": {"message": None, "desc": "The request exceeded the rate limit."},
}

status_code_general = {
    "429": {"message": None, "desc": "The request exceeded the rate limit."},
}
HEADERS = {"User-Agent": f"python-sxcu-{__version__}"}
