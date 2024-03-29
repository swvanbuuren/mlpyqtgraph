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
import sphinx_immaterial
#import pathlib as pl
#sys.path.insert(0, pl.Path(__file__).parents[2].absolute())
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, '..', '..'))
import mlpyqtgraph


# -- Project information -----------------------------------------------------

project = 'mlpyqtgraph'
copyright = '2022, Sietze van Buuren'
author = 'Sietze van Buuren'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_immaterial',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_immaterial'

# material theme options (see theme.conf for more information)
html_theme_options = {
    'toc_title': 'Page Contents',
    'features': [
        'navigation.expand',
        # 'navigation.tabs',
        'navigation.sections',
        # 'navigation.instant',
        # 'header.autohide',
        'navigation.top',
        # 'navigation.tracking',
        # 'search.highlight',
        'search.share',
        'toc.follow',
        'toc.sticky',
        'content.tabs.link',
        'announce.dismiss',
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

rst_epilog = """
.. role:: raw-html(raw)
   :format: html
.. |pyqtgraph| replace:: :raw-html:`<a href="https://github.com/pyqtgraph/pyqtgraph">pyqtgraph</a>`
.. |matplotlib| replace:: :raw-html:`<a href="https://matplotlib.org">matplotlib</a>`
"""
