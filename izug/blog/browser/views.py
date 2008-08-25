from Products.Five.browser import BrowserView
from zope.interface import implements
from izug.blog.interfaces import IBlogView, IBlogEntryView, IBlog
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

class BlogEntryView(BrowserView):
    implements(IBlogEntryView)
    """
    """
    
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
        
        if context.Type() in ['Blog','Topic', 'Collection']:
            return self.template()
        else:
            querystring = context.REQUEST.get('QUERY_STRING','')
            querystring = querystring and '?' + querystring or querystring
            
            level = context
            while not IBlog.providedBy(level):
                level = level.aq_parent
            
            url = level.absolute_url() + querystring
            self.context.REQUEST.RESPONSE.redirect(url)
