"""Definition of the simplelayout based Blog Entry content type
"""

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from DateTime import DateTime
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from zope.interface import implements

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType

from ftw.blog.interfaces import ISlBlogEntry
from ftw.blog.config import PROJECTNAME
from ftw.blog import _
from simplelayout.base.interfaces import ISimpleLayoutCapable


SlBlogEntrySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.ReferenceField(
        name='categories',
        required=False,
        widget=ReferenceBrowserWidget(
            label=_('Categories'),
            allow_browse=False,
            show_results_without_query=True,
            restrict_browsing_to_startup_directory=True,
            base_query={"portal_type": "BlogCategory",
                        "sort_on": "sortable_title"},
            macro='category_reference_widget',
        ),
        multiValued=1,
        schemata='default',
        relationship='blog_categories',
        allowed_types=['BlogCategory'],
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(SlBlogEntrySchema,
                            folderish=True,
                            moveDiscussion=False)

# #hide some fields
SlBlogEntrySchema['subject'].widget.visible = -1
SlBlogEntrySchema.changeSchemataForField('subject', 'default')
SlBlogEntrySchema['location'].widget.visible = -1
SlBlogEntrySchema.changeSchemataForField('location', 'default')
SlBlogEntrySchema['language'].widget.visible = -1
SlBlogEntrySchema.changeSchemataForField('language', 'default')


class SlBlogEntry(folder.ATFolder):
    """Ftw Blog Entry"""
    implements(ISlBlogEntry, ISimpleLayoutCapable)
    security = ClassSecurityInfo()

    portal_type = "SlBlogEntry"
    schema = SlBlogEntrySchema

    #returns the category uid and the parent category uid
    def getCategoryUids(self):
        cats = aq_inner(self).getCategories()
        uids = [c.UID() for c in cats]
        parent_uids = []
        for pc in cats:
            parent = aq_inner(pc).aq_parent
            puid = parent.UID()
            grand_parent = aq_inner(parent).aq_parent
            if puid not in parent_uids \
                and grand_parent.Type() == 'Blog Category':
                parent_uids.append(puid)
                DateTime(self.CreationDate()).strftime('%m/%Y')
        return parent_uids + uids

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        return False


registerType(SlBlogEntry, PROJECTNAME)
