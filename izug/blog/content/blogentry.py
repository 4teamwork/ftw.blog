"""Definition of the Blog Item content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from izug.blog import blogMessageFactory as _
from izug.blog.interfaces import IBlogEntry
from izug.blog.config import PROJECTNAME


from izug.contentpage.content.contentpage import ContentPage, ContentPageSchema


BlogEntrySchema = ContentPageSchema.copy()

schemata.finalizeATCTSchema(BlogEntrySchema, folderish=True, moveDiscussion=False)

#inherid from izug.contentpage

class BlogEntry(ContentPage):
    """iZug Blog Entry"""
    implements(IBlogEntry)

    portal_type = "Blog Entry"
    schema = BlogEntrySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(BlogEntry, PROJECTNAME)
