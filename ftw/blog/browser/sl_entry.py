from ftw.blog.browser.entry import BlogEntryView
from ftw.blog.interfaces import ISlBlogEntryView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class SlBlogEntryView(BlogEntryView):
    """ The Blog entry detail View. """

    implements(ISlBlogEntryView)

    template = ViewPageTemplateFile("sl_entry.pt")
