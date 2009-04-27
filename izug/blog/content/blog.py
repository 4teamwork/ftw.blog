"""Definition of the Blog content type
"""

from zope.interface import implements, directlyProvides
from zope.interface import alsoProvides, noLongerProvides

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent, View, ManagePortal
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from izug.blog import blogMessageFactory as _
from izug.blog.interfaces import IBlog
from izug.blog.config import PROJECTNAME

from izug.tagging.interfaces.tagging import ITagRoot
from izug.arbeitsraum.content.utilities import finalizeIzugSchema

BlogSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.BooleanField('tag_root',
        default = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.BooleanWidget(label = _(u'label_blog_tag_root', default=u"Tag Root"),
                                     description = _(u'help_blog_tag_root', default=u""),
        )
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BlogSchema['title'].storage = atapi.AnnotationStorage()
BlogSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BlogSchema, folderish=True, moveDiscussion=False)
finalizeIzugSchema(BlogSchema, folderish=True, moveDiscussion=False)
BlogSchema['effectiveDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}
BlogSchema['expirationDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}

BlogSchema['tag_root'].write_permission = ManagePortal

# hide schematas ..
for field in BlogSchema.keys():
    if BlogSchema[field].schemata in ['categorization']:
        BlogSchema[field].widget.visible['edit'] = 'invisible'

class Blog(folder.ATFolder):
    """iZug Blog"""
    implements(IBlog)

    portal_type = "Blog"
    schema = BlogSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    tag_root = atapi.ATFieldProperty('tag_root')

    security = ClassSecurityInfo()

    security.declareProtected(View, 'getTag_root')
    def getTag_root(self):
        if ITagRoot.providedBy(self):
            return True
        else:
            return False

    security.declareProtected(ModifyPortalContent, 'setTag_root')
    def setTag_root(self, value, **kwargs):
        field = self.getField('tag_root')
        field.set(self, value, **kwargs)
        
        if value:
            alsoProvides(self, ITagRoot)
        else:
            noLongerProvides(self, ITagRoot)

atapi.registerType(Blog, PROJECTNAME)
