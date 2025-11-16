# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RoboEval'
copyright = '2025, Yi Ru Wang, Carter Ung, et al.'
author = 'Yi Ru Wang, Carter Ung, et al.'
release = '4.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

html_title = "RoboEval Documentation"

html_theme_options = {
    # Show the site's top-level sections in the left sidebar on all pages.
    "home_page_in_toc": True,
    # How many levels of the TOC to show in the navbar/sidebar.
    "show_navbar_depth": 2,
    "repository_url": "https://github.com/helen9975/RoboEval",
    "use_repository_button": True,
}

html_css_files = [
    'css/custom.css'
]

# Cache busting for static files during development
import time
html_context = {
    'build_time': int(time.time())  # Add timestamp to force cache refresh
}

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'gymnasium': ('https://gymnasium.farama.org/', None),
}
