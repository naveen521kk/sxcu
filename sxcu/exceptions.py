"""Custom Exeeption declarations.
"""


class SXCUError(Exception):
    """SXCUError A error which will be raised when the returned status
    code isn't right.

    See error_codes and message list for more information in
    https://sxcu.net.
    """
