from .sxcu import SXCU, og_properties  # noqa F401

try:
    from importlib.metadata import version as importlib_metadata_version
except ImportError:
    from importlib_metadata import version as importlib_metadata_version

__version__ = importlib_metadata_version("sxcu")
