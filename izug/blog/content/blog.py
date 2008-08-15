"""Definition of the Blog content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from izug.blog import blogMessageFactory as _
from izug.blog.interfaces import IBlog
from izug.blog.config import PROJECTNAME

BlogSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BlogSchema['title'].storage = atapi.AnnotationStorage()
BlogSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BlogSchema, folderish=True, moveDiscussion=False)

class Blog(folder.ATFolder):
    """iZug Blog"""
    implements(IBlog)

    portal_type = "Blog"
    schema = BlogSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Blog, PROJECTNAME)
