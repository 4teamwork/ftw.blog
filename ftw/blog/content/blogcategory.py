"""Definition of the Blog Category content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from ftw.blog.interfaces import IBlogCategory
from ftw.blog.config import PROJECTNAME

BlogCategorySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(BlogCategorySchema,
                            folderish=True,
                            moveDiscussion=False)

BlogCategorySchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                                      'edit': 'invisible'}
BlogCategorySchema['expirationDate'].widget.visible = {'view': 'invisible',
                                                       'edit': 'invisible'}


class BlogCategory(folder.ATFolder):
    """iZug Blog Category"""
    implements(IBlogCategory)

    portal_type = "BlogCategory"
    schema = BlogCategorySchema

atapi.registerType(BlogCategory, PROJECTNAME)
