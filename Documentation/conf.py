import pydata_sphinx_theme

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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Mecha Karen'
copyright = '2021, Seniatical'
author = 'Seniatical'

# The full version, including alpha/beta/rc tags
release = '1.9.2a'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
## extensions = ['sphinx_rtd_theme']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['*.md', '*.template']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'
html_logo = "_static/karen.png"

html_theme_options = {
   "favicons": [
      {
         "rel": "icon",
         "sizes": "16x16",
         "href": "karen.png",
      },
      {
         "rel": "icon",
         "sizes": "32x32",
         "href": "karen.png",
      },
      {
         "rel": "apple-touch-icon",
         "sizes": "180x180",
         "href": "karen.png"
      },
   ],

   "icon_links": [
      {
         "name": "GitHub",
         "url": "https://github.com/Seniatical/Mecha-Karen/",
         "icon": "fab fa-github",
      },
      {
         "name": "Discord",
         "url": "https://discord.com/invite/Q5mFhUM",
         "icon": "fab fa-discord"
      },
      {
         "name": "Dashboard",
         "url": "https://mechakaren.xyz/dashboard",
         "icon": "fas fa-box"
      }
    ],

   "use_edit_page_button": True,
   "collapse_navigation": False,
   "navigation_depth": 3,
   "search_bar_text": "Search the docs ...",
   "footer_items": ["copyright", "sphinx-version", "last-updated"],

}

html_context = {
    "github_url": "https://github.com",
    "github_user": "Seniatical",
    "github_repo": "Mecha-Karen",
    "github_version": "main",
    "doc_path": "Documentation",
}

html_sidebars = {
    "**": ["search-field", "sidebar-nav-bs"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]