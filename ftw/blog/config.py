"""Common configuration constants
"""

PROJECTNAME = 'ftw.blog'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'BlogEntry': 'ftw.blog: Add BlogEntry',
    'BlogCategory': 'ftw.blog: Add BlogCategory',
    'Blog': 'ftw.blog: Add Blog',
}

# TODO: is that index possible or only the metadata
INDEXES = (("getCategoryUids", "KeywordIndex"),
          )

METADATA = ('getCategoryUids',)

TINYMCE_ALLOWED_BUTTONS = (
    'bg-basicmarkup',
    'bold-button',
    'italic-button',
    'list-ol-addbutton',
    'list-ul-addbutton',
    'definitionlist',
    'linklibdrawer-button',
    'removelink-button',
    'tabledrawer-button'
    

)

product_globals = globals()
