# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Add the path to your source code
sys.path.insert(0, os.path.abspath('../../pyharmonics/src'))
print(f"Current working directory: {os.getcwd()}")
print(f"Added to sys.path: {os.path.abspath('../../')}")

project = 'Pyharmonics'
copyright = "2025, Niall O'Connor"
author = "Niall O'Connor"
release = '1.4.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Automatically extract docstrings
    'sphinx.ext.viewcode',  # Add links to source code
    'sphinx.ext.napoleon',  # Support for Google/NumPy-style docstrings
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
