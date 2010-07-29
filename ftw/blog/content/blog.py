"""Definition of the Blog content type
"""

from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ManagePortal
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from ftw.blog import _
from ftw.blog.interfaces import IBlog
from ftw.blog.config import PROJECTNAME

BlogSchema = folder.ATFolderSchema.copy() + atapi.Schema((

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BlogSchema['title'].storage = atapi.AnnotationStorage()
BlogSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BlogSchema, folderish=True, moveDiscussion=False)
### REMOVED because its not necessary
# # finalizeZugSchema(BlogSchema, folderish=True, moveDiscussion=False)
BlogSchema['effectiveDate'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
BlogSchema['expirationDate'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}

# hide schematas ..
for field in BlogSchema.keys():
    if BlogSchema[field].schemata in ['categorization']:
        BlogSchema[field].widget.visible['edit'] = 'invisible'


class Blog(folder.ATFolder):
    """ftw Blog"""
    implements(IBlog)

    portal_type = "Blog"
    schema = BlogSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()

atapi.registerType(Blog, PROJECTNAME)
