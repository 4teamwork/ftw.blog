"""Common configuration constants
"""

PROJECTNAME = 'ftw.blog'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'BlogEntry': 'ftw.blog: Add BlogEntry',
    'BlogCategory': 'ftw.blog: Add BlogCategory',
    'Blog': 'ftw.blog: Add Blog',
}

INDEXES = (("getCategoryUids", "KeywordIndex"),
           ("getTeaserText", "FieldIndex"),
           ("InfosForArchiv", "FieldIndex"),
          )

METADATA = ('getCategoryUids', 'getTeaserText', 'InfosForArchiv')

product_globals = globals()
