"""Definition of the Blog Entry content type
"""
from zope.interface import implements
from Acquisition import aq_inner
from DateTime import DateTime
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget import ATReferenceBrowserWidget

from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import registerType
else:
    from Products.Archetypes.atapi import registerType

from ftw.blog.interfaces import IBlogEntry
from ftw.blog.config import PROJECTNAME, TINYMCE_ALLOWED_BUTTONS
from ftw.blog import _

BlogEntrySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.TextField(
        name='text',
        storage=atapi.AnnotationStorage(),
        schemata='default',
        required=False,
        searchable=True,
        default_input_type='text/html',
        default_output_type='text/html',
        widget=atapi.RichWidget(
            label='Text',
            label_msgid='ftw_label_text',
            description='',
            description_msgid='ftw_help_text',
            i18n_domain='ftw.tagging',
            rows=15,
            allow_buttons=TINYMCE_ALLOWED_BUTTONS,
            rooted=True,
        ),
    ),

    atapi.ReferenceField(
        name='categories',
        required=False,
        widget=ATReferenceBrowserWidget.ReferenceBrowserWidget(
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


class BlogEntry(folder.ATFolder):
    """Ftw Blog Entry"""
    implements(IBlogEntry)

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


registerType(BlogEntry, PROJECTNAME)
