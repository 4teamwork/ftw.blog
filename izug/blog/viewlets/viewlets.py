from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.globals.interfaces import IViewView 
from zope.interface import implements, alsoProvides
from plone.app.layout.viewlets.comments import CommentsViewlet

class izugBlogActionsBar(ViewletBase):
    render = ViewPageTemplateFile('izug_blog_actionsbar.pt')

    def update(self):
        context = aq_inner(self.context)
        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        self.object_actions = context_state.actions().get('blog_actions', [])

        plone_utils = getToolByName(context, 'plone_utils')

        self.portal_actionicons = getToolByName(context, 'portal_actionicons')
        
        # The drop-down menus are pulled in via a simple content provider
        # from plone.app.contentmenu. This behaves differently depending on
        # whether the view is marked with IViewView. If our parent view 
        # provides that marker, we should do it here as well.
        if IViewView.providedBy(self.__parent__):
            alsoProvides(self, IViewView)
            
            
class izugBlogNavigation(ViewletBase):
    render = ViewPageTemplateFile('izug_blog_navigation.pt')
    
    def update(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        catalog = getToolByName(context,'portal_catalog')

        query = {}
        query['portal_type'] = 'Blog Entry'
        query['sort_on'] = 'created'
        query['path'] = '/'.join(parent.getPhysicalPath())
        results = catalog(query)

        uids = [b.UID for b in results]
        current_uid = context.UID()
        current_index = uids.index(current_uid)
        #we have to convert the new indexes to strings, otherwhise this two lines blow will no work correctly
        prev_index = current_index != 0 and str(current_index - 1) or False
        next_index = current_index != len(uids)-1 and str(current_index+1) or False
        
        if prev_index:
            prev = dict(title=self.cropTitle(results[int(prev_index)].Title),
                        url = results[int(prev_index)].getURL())
        if next_index:
            next = dict(title=self.cropTitle(results[int(next_index)].Title),
                        url = results[int(next_index)].getURL())
        self.prev = prev_index and prev
        self.next = next_index and next
            
    def cropTitle(self,title):
        return len(title) > 20 and title[:20] + '... ' or title
        
class CommentsViewlet(CommentsViewlet):
    render = ViewPageTemplateFile('izug_comments.pt')