"""
    __logger__.py
    ~~~~~~~~~~~~~

    Simple defines the logger used across the module.

"""

import logging

logger = logging.getLogger("sxcu")
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)
s_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
s_handler.setFormatter(s_format)
logger.addHandler(s_handler)
