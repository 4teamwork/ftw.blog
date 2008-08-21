from Products.Five.browser import BrowserView
from zope.interface import implements
from izug.blog.interfaces import IBlogView, IBlogEntryView


class BlogEntryView(BrowserView):
    implements(IBlogEntryView)
    """
    """
    
class BlogView(BrowserView):
    implements(IBlogView)
    """
    Uses default plone folder_listing.pt as base
    everything is in the template.
    It works with Topics too
    """
