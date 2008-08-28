from Products.Five.browser import BrowserView
from zope.interface import implements
from izug.blog.interfaces import IBlogView, IBlogEntryView, IBlog
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

class BlogEntryView(BrowserView):
    implements(IBlogEntryView)
    template=ViewPageTemplateFile("blog_entry_view.pt")
    
    def __call__(self):
        context = aq_inner(self.context).aq_explicit
        context.REQUEST.set('disable_border',1)
        return self.template()
    
class BlogView(BrowserView):
    implements(IBlogView)
    """
    Uses default plone folder_listing.pt as base
    nearly everything is in the template.
    It works with Topics too
    """
    template=ViewPageTemplateFile("blog_view.pt")

    def __call__(self):
        context = aq_inner(self.context).aq_explicit
        req = context.REQUEST
        #hide the green contentmenu-bar
        req.set('disable_border',1)
        
        
        if context.Type() == 'Collection':
            return self.template()
        elif context.Type() == 'Blog':
            #set some default blog query options
            req.set('sort_on','created')
            req.set('sort_order','reverse')
            req.set('portal_type','Blog Entry')
            limit_display = req.get('limit_display',5)
            req.set('limit_display',limit_display)
            b_start = req.get('b_start',0)
            req.set('b_start',b_start)

            return self.template()
            
        else:
            querystring = context.REQUEST.get('QUERY_STRING','')
            querystring = querystring and '?' + querystring or querystring
            
            level = context
            while not IBlog.providedBy(level):
                level = level.aq_parent
            
            url = level.absolute_url() + querystring
            self.context.REQUEST.RESPONSE.redirect(url)
            
            
class createBlogEntryPath(BrowserView):

    def URL(self):
        level = aq_inner(self.context).aq_explicit
        while not IBlog.providedBy(level):
            level = level.aq_parent
        return '%s/createObject?type_name=Blog+Entry' % level.absolute_url()


class BlogSettings(BrowserView):
    def objectActions(self):
        context = aq_inner(self.context)
        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        return context_state.actions().get('blog_settings_actions', [])
        
    def categoriesUrl(self):
        level = aq_inner(self.context).aq_explicit
        while not IBlog.providedBy(level):
            level = level.aq_parent
        return '%s/categories' % level.absolute_url()

    def managePortletUrl(self):
        level = aq_inner(self.context).aq_explicit
        while not IBlog.providedBy(level):
            level = level.aq_parent
        return '%s/@@manage-blog-portlets' % level.absolute_url()

    def editBlog(self):
        level = aq_inner(self.context).aq_explicit
        while not IBlog.providedBy(level):
            level = level.aq_parent
        return '%s/edit' % level.absolute_url()
    
