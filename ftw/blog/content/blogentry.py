"""Definition of the Blog Entry content type
"""

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from DateTime import DateTime
from ftw.blog import _
from ftw.blog.config import PROJECTNAME
from ftw.blog.interfaces import IBlogEntry
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.interface import implements

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType


BlogEntrySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.TextField(
        name='text',
        storage=atapi.AnnotationStorage(),
        schemata='default',
        required=False,
        searchable=True,
        allowable_content_types=('text/html', ),
        default_content_type='text/html',
        validators=('isTidyHtmlWithCleanup', ),
        default_input_type='text/html',
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label='Text',
            label_msgid='ftw_label_text',
            description='',
            description_msgid='ftw_help_text',
            i18n_domain='ftw.tagging',
            rows=15,
            rooted=True,
        ),
    ),

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

    atapi.BooleanField(
        name='showImages',
        required=False,
        default=True,
        schemata='default',
        widget=atapi.BooleanWidget(
            label=_('label_show_images', default=u'Show images as gallery'),
            description=_('description_show_images',
                           default=u'Decide you want to show all uploaded '
                                    'images as gallery'),
        ),
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(BlogEntrySchema,
                            folderish=True,
                            moveDiscussion=False)
#finalizeZugSchema(BlogEntrySchema, folderish=True, moveDiscussion=False)
BlogEntrySchema['effectiveDate'].widget.visible = {'view': 'invisible',
                                                    'edit': 'invisible'}
BlogEntrySchema['expirationDate'].widget.visible = {'view': 'invisible',
                                                    'edit': 'invisible'}

# #hide some fields
BlogEntrySchema['subject'].widget.visible = -1
BlogEntrySchema.changeSchemataForField('subject', 'default')
BlogEntrySchema['location'].widget.visible = -1
BlogEntrySchema.changeSchemataForField('location', 'default')
BlogEntrySchema['language'].widget.visible = -1
BlogEntrySchema.changeSchemataForField('language', 'default')
BlogEntrySchema['description'].widget.visible = -1

#protect fields; they should only be editable for managers
protected_fields = ['creators', 'contributors', 'rights', 'allowDiscussion',
                    'excludeFromNav', 'nextPreviousEnabled']
for fieldname in protected_fields:
    if fieldname in BlogEntrySchema:
        BlogEntrySchema[fieldname].write_permission = 'Manage portal'

BlogEntrySchema.addField(schemata.relatedItemsField.copy())


class BlogEntry(folder.ATFolder):
    """Ftw Blog Entry"""
    implements(IBlogEntry)
    security = ClassSecurityInfo()

    portal_type = "BlogEntry"
    schema = BlogEntrySchema

    text = atapi.ATFieldProperty('text')

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


registerType(BlogEntry, PROJECTNAME)
