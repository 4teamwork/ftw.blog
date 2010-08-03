from Products.Five.browser import BrowserView
from zope.interface import implements
from ftw.blog.interfaces import IBlogView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.content.batching import Batch
from Acquisition import aq_inner, aq_parent


class BlogView(BrowserView):
    implements(IBlogView)
    """ Shows a Listing of all Blog entries, with the corresponding portlets."""

    template=ViewPageTemplateFile("blog.pt")

    batching=ViewPageTemplateFile("batching.pt")

    def __call__(self):
        """ Get all the Blogentries and return the listingview template."""

        context = aq_inner(self.context).aq_explicit
        req = context.REQUEST

        if context.portal_type != 'Blog':
            return self.context.REQUEST.RESPONSE.redirect(
                aq_parent(aq_inner(self.context)).absolute_url())

        self.entries = self.context.getFolderContents({
            'sort_on': 'created',
            'sort_order': 'reverse',
            'portal_type': 'BlogEntry'})

        pagesize = int(req.get('pagesize', 5))
        req.set('pagesize', pagesize)
        pagenumber = int(req.get('pagenumber', 1))
        req.set('pagenumber', pagenumber)

        self.batch = Batch(self.entries,
            pagesize=pagesize, pagenumber=pagenumber, navlistsize=1)

        return self.template()
