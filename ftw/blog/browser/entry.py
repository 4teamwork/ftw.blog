from Products.Five.browser import BrowserView
from zope.interface import implements
from ftw.blog.interfaces import IBlogEntryView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class BlogEntryView(BrowserView):
    """ The Blog entry detail View. """

    implements(IBlogEntryView)
    template=ViewPageTemplateFile("entry.pt")

    def __call__(self):
        return self.template()
