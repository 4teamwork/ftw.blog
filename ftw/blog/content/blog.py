"""Definition of the Blog content type
"""
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType

from ftw.blog.interfaces import IBlog
from ftw.blog.config import PROJECTNAME


BlogSchema = folder.ATFolderSchema.copy()
schemata.finalizeATCTSchema(BlogSchema, folderish=True, moveDiscussion=False)


class Blog(folder.ATFolder):
    """The Ftw Blog Type"""
    implements(IBlog)

    portal_type = "Blog"
    schema = BlogSchema

    security = ClassSecurityInfo()

registerType(Blog, PROJECTNAME)
