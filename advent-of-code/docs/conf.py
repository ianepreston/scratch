"""Sphinx configuration."""
project = "Ian's Advent of Code"
author = "Ian Preston"
copyright = "2022, Ian Preston"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
