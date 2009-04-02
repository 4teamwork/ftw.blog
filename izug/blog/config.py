"""Common configuration constants
"""

PROJECTNAME = 'izug.blog'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Blog Entry': 'izug.blog: Add Blog Entry',
    'Blog Category': 'izug.blog: Add Blog Category',
    'Blog': 'izug.blog: Add Blog',
}

INDEXES = (("getCategoryUids", "KeywordIndex"),
           ("getTeaserText", "FieldIndex"),
           ("InfosForArchiv", "FieldIndex"),
          )
          
METADATA = ('getCategoryUids', 'getTeaserText', 'InfosForArchiv')

product_globals = globals()
