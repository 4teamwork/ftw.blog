"""Definition of the Blog Category content type
"""
from zope.interface import implements
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType

from ftw.blog.interfaces import IBlogCategory
from ftw.blog.config import PROJECTNAME


BlogCategorySchema = folder.ATFolderSchema.copy()
schemata.finalizeATCTSchema(BlogCategorySchema,
                            folderish=True,
                            moveDiscussion=False)


class BlogCategory(folder.ATFolder):
    """Blog Category"""
    implements(IBlogCategory)

    portal_type = "BlogCategory"
    schema = BlogCategorySchema

registerType(BlogCategory, PROJECTNAME)
