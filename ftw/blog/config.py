"""Common configuration constants
"""

PROJECTNAME = 'ftw.blog'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'BlogEntry': 'ftw.blog: Add BlogEntry',
    'BlogCategory': 'ftw.blog: Add BlogCategory',
    'Blog': 'ftw.blog: Add Blog',
    }

INDEXES = (
    ("getCategoryUids", "KeywordIndex"),
    )

product_globals = globals()
