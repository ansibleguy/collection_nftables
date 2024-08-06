from datetime import datetime

# pylint: disable=W0622

project = 'Ansible Collection - NFTables'
copyright = f'{datetime.now().year}, AnsibleGuy'
author = 'AnsibleGuy'
extensions = ['piccolo_theme']
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'piccolo_theme'
html_static_path = ['_static']
html_logo = 'https://netfilter.org/images/netfilter-logo3.png'
html_favicon = '_static/img/logo.png'
html_css_files = ['css/main.css']
master_doc = 'index'
display_version = True
sticky_navigation = True
source_suffix = {
    '.rst': 'restructuredtext',
}
html_theme_options = {}
html_short_title = 'Ansible NFTables'
