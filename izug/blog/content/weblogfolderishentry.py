"""Definition of the Block content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.Quills.WeblogEntry import WeblogEntry, WeblogEntrySchema

from izug.blog import blogMessageFactory as _
from izug.blog.interfaces import IWeblogFolderishItem
from izug.blog.config import PROJECTNAME

WeblogFolderishEntrySchema = folder.ATFolderSchema.copy() + WeblogEntrySchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

#BlockSchema['title'].storage = atapi.AnnotationStorage()
#BlockSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(WeblogFolderishEntrySchema, folderish=True, moveDiscussion=False)

class WeblogFolderishEntry(folder.ATFolder, WeblogEntry):
    """WeblogFolderishEntry"""
    implements(IWeblogFolderishItem)

    portal_type = "WeblogFolderishEntry"
    schema = WeblogFolderishEntrySchema

    #title = atapi.ATFieldProperty('title')
    #description = atapi.ATFieldProperty('description')

atapi.registerType(WeblogFolderishEntry, PROJECTNAME)
