# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from importlib.metadata import version as importlib_metadata_version

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------
project = "SXCU"
copyright = "2020, Naveen M K"
author = "Naveen M K"

# The full version, including alpha/beta/rc tags
release = importlib_metadata_version("sxcu")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

import sphinx_rtd_theme  # noqa:E402,F401

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    "analytics_id": "UA-140820927-3",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "style_nav_header_background": "black",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "logo.png"
html_favicon = "favicon.ico"

autosummary_generate = True
master_doc = "index"
