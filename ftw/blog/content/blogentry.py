"""Definition of the Blog Entry content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from ftw.blog.interfaces import IBlogEntry
from ftw.blog.config import PROJECTNAME
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
            label='Body Text',
            label_msgid='izug_label_text',
            description='',
            description_msgid='izug_help_text',
            i18n_domain='izug',
            rows=25,
        ),
    ),

    atapi.ReferenceField(
        name='categories',
        required=True,
        widget=ReferenceBrowserWidget(
            label=_('Categories'),
            allow_browse=False,
            show_results_without_query=True,
            restrict_browsing_to_startup_directory=True,
            base_query={"portal_type": "Blog Catgory",
                        "sort_on": "sortable_title"},
            macro='category_reference_widget',
        ),
        allowed_types=('ClassificationItem', ),
        multiValued=1,
        schemata='default',
        relationship='blog_categories'
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BlogEntrySchema['title'].storage = atapi.AnnotationStorage()
BlogEntrySchema['description'].storage = atapi.AnnotationStorage()

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

# #move schemata  
# ms = atapi.ManagedSchema(BlogEntrySchema.fields())
# ms.moveSchemata('default',-1)
# 
# schemata.finalizeATCTSchema(ms, folderish=True, moveDiscussion=False)
# 
# ms.changeSchemataForField('effectiveDate','settings')
# ms.changeSchemataForField('expirationDate','settings')
# ms['effectiveDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}
# ms['expirationDate'].widget.visible = {'view' : 'invisible', 'edit' : 'invisible'}


class BlogEntry(folder.ATFolder):
    """Ftw Blog Entry"""
    implements(IBlogEntry)

    portal_type = "BlogEntry"
    schema = BlogEntrySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(BlogEntry, PROJECTNAME)
