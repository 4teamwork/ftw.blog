"""Definition of the Blog content type
"""
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType

from ftw.blog.interfaces import IBlog
from ftw.blog.config import PROJECTNAME

BlogSchema = folder.ATFolderSchema.copy() + atapi.Schema((

))

schemata.finalizeATCTSchema(BlogSchema, folderish=True, moveDiscussion=False)

BlogSchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                              'edit': 'invisible'}
BlogSchema['expirationDate'].widget.visible = {'view': 'invisible',
                                               'edit': 'invisible'}

# hide schematas ..
for field in BlogSchema.keys():
    if BlogSchema[field].schemata in ['categorization']:
        BlogSchema[field].widget.visible['edit'] = 'invisible'


class Blog(folder.ATFolder):
    """The Ftw Blog Type"""
    implements(IBlog)

    portal_type = "Blog"
    schema = BlogSchema

    security = ClassSecurityInfo()

registerType(Blog, PROJECTNAME)
