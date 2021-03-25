"""
    __logger__.py
    ~~~~~~~~~~~~~

    Simple defines the logger used across the module.

"""
__all__ = ["logger"]

import logging

logger = logging.getLogger("sxcu")  # pylint: disable=invalid-name
S_HANDLER = logging.StreamHandler()
S_HANDLER.setLevel(logging.DEBUG)
S_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
S_HANDLER.setFormatter(S_FORMAT)
logger.addHandler(S_HANDLER)
