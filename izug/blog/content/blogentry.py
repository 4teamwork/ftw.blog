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
    
    #returns the category uid and the parent category uid
    def getCategoryUids(self):
        cats = self.getCategories()
        uids = [c.UID() for c in cats]
        parent_uids = []
        for pc in cats:
            puid = aq_inner(pc).aq_parent.UID()
            if puid not in parent_uids:
                parent_uids.append(puid)
                
        return parent_uids + uids
    
    #returns teaser text for blog listing
    def getTeaserText(self):
        contents = self.listFolderContents(contentFilter={'portal_type':'Block'})
        if not contents:
            return ''
        
        first_block = contents[0]
        block_text = first_block.getText()
        teaser_text = len(block_text) > 200 and block_text[200:] + ' ...' or block_text
        return teaser_text 
    
    

atapi.registerType(BlogEntry, PROJECTNAME)
