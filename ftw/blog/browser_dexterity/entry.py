from Products.Five.browser import BrowserView
from five import grok
from zope.interface import implements

from ftw.blog.interfaces import IBlogEntryView
from ftw.tagging.behaviors.tagging import ITaggableSchema


class BlogEntryView(BrowserView):
    """This view renders a list of blog entries.
    """

    implements(IBlogEntryView)

    def get_tags(self):
        return ITaggableSchema(self.context).tags


class MyAdapter(grok.Adapter):
    pass
