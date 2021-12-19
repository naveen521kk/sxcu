"""
    __logger__.py
    ~~~~~~~~~~~~~

    Simple defines the logger used across the module.

"""
__all__ = ["logger"]

import logging

logger = logging.getLogger("sxcu")  # pylint: disable=invalid-name
