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
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget


schema = atapi.Schema((
    atapi.ReferenceField(
        name='categories',
        widget=ReferenceBrowserWidget(
            label=_('Categories'),
            allow_browse=False,
            show_results_without_query=True,
            restrict_browsing_to_startup_directory=True,
            base_query={"portal_type": "Blog Catgory", "sort_on": "sortable_title"},
            macro='category_reference_widget',
        ),
        allowed_types=('ClassificationItem',),
        multiValued=1,
        schemata='categorization',
        relationship='blog_categories'
    ),


))

BlogEntrySchema = schema.copy() + ContentPageSchema.copy()

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
