from Products.Five.browser import BrowserView
from zope.interface import implements
from ftw.blog.interfaces import IBlogEntryView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.tagging.utils import getInterfaceRoot
from ftw.tagging.interfaces.tagging import ITagRoot


class BlogEntryView(BrowserView):
    """ The Blog entry detail View. """

    implements(IBlogEntryView)
    template=ViewPageTemplateFile("entry.pt")

    def __call__(self):
        self.tag_root = getInterfaceRoot(self.context, ITagRoot)
        return self.template()
