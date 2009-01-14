"""Definition of the Blog Item content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata


from izug.blog import blogMessageFactory as _
from izug.blog.interfaces import IBlogEntry
from izug.blog.config import PROJECTNAME
from Acquisition import aq_inner
from Products.AddRemoveWidget import AddRemoveWidget
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime


from izug.contentpage.content.contentpage import ContentPage, ContentPageSchema
from izug.block.content.block import Block, BlockSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget


schema = atapi.Schema((
    atapi.ReferenceField(
        name='categories',
        required=True,
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
        schemata='default',
        relationship='blog_categories'
    ),

))

BlogEntrySchema = schema.copy() + ContentPageSchema.copy() + BlockSchema.copy()

#hide some fields
if BlogEntrySchema.has_key('subject'):
    BlogEntrySchema['subject'].widget.visible = -1
if BlogEntrySchema.has_key('location'):
    BlogEntrySchema['location'].widget.visible = -1
if BlogEntrySchema.has_key('language'):
    BlogEntrySchema['language'].widget.visible = -1    

BlogEntrySchema['title'].required = 1
BlogEntrySchema['title'].searchable = 1
BlogEntrySchema['description'].widget.visible = 1

if BlogEntrySchema.has_key('showTitle'):
    BlogEntrySchema['showTitle'].default = 1
    BlogEntrySchema['showTitle'].widget.visible = -1

BlogEntrySchema.moveField('categories', pos='bottom')

#move schemata  
ms = atapi.ManagedSchema(BlogEntrySchema.fields())
ms.moveSchemata('default',-1)

schemata.finalizeATCTSchema(ms, folderish=True, moveDiscussion=False)

#inherid from izug.contentpage

class BlogEntry(Block,ContentPage):
    """iZug Blog Entry"""
    implements(IBlogEntry)

    portal_type = "Blog Entry"
    schema = ms

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    #returns the category uid and the parent category uid
    def getCategoryUids(self):
        cats = aq_inner(self).getCategories()
        uids = [c.UID() for c in cats]
        parent_uids = []
        for pc in cats:
            parent = aq_inner(pc).aq_parent
            puid = parent.UID()
            grand_parent = aq_inner(parent).aq_parent
            if puid not in parent_uids and grand_parent.Type()=='Blog Category':
                parent_uids.append(puid)
                DateTime(self.CreationDate()).strftime('%m/%Y')
        return parent_uids + uids
    
    #returns teaser text for blog listing
    def getTeaserText(self):
        
        block_text = self.getText()
    
        teaser_text = len(block_text) > 200 and block_text[:200] + '...' or block_text
        return teaser_text 
    
    def InfosForArchiv(self):
        return DateTime(self.CreationDate()).strftime('%m/01/%Y')


atapi.registerType(BlogEntry, PROJECTNAME)
