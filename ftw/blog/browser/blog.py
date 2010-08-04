from Products.Five.browser import BrowserView
from zope.interface import implements
from ftw.blog.interfaces import IBlogView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.content.batching import Batch
from Acquisition import aq_inner, aq_parent
from DateTime import DateTime

class BlogView(BrowserView):
    implements(IBlogView)
    """ Shows a Listing of all Blog entries, with the corresponding portlets."""

    template=ViewPageTemplateFile("blog.pt")

    batching=ViewPageTemplateFile("batching.pt")

    filters = []

    def __call__(self):
        """ Get all the Blogentries and return the listingview template.
        
        If there was a CategoryUid or a date in the querystring,
        the results would be filtered.
        
        """
        
        context = aq_inner(self.context).aq_explicit
        req = context.REQUEST
        query = {}
        self.filters = []
        querystring = context.REQUEST.get('QUERY_STRING', '')
        
        if querystring:
            if 'archiv' in querystring:
                datestr = querystring[querystring.find('archiv=')+ 7:]
                start = DateTime(datestr)
                end = DateTime('%s/%s/%s' % (start.year(), start.month()+ 1, start.day()))
                end = end - 1
                query['created'] = {'query':(start, end), 'range': 'min:max'}
                self.filters.append(start.strftime('%B %Y'))

            if 'getCategoryUids' in querystring:
                uid = querystring.split('=')[1]
                query['getCategoryUids'] = uid
                category = self.context.portal_catalog(UID=uid)[0]
                self.filters.append(category.Title)
            if 'searchable_text' in querystring:
                searchable_text = querystring.split('=')[1]
                searchable_text = searchable_text[:searchable_text.find('&')]
                query['SearchableText'] = searchable_text
                self.filters.append(searchable_text)

        if context.portal_type != 'Blog':
            if querystring:
                querystring = '?%s' % querystring
            return self.context.REQUEST.RESPONSE.redirect(
                aq_parent(aq_inner(self.context)).absolute_url()+ querystring)

        query['sort_on'] = 'created'
        query['sort_order'] = 'reverse'
        query['portal_type'] = 'BlogEntry'
        self.entries = self.context.getFolderContents(contentFilter=query)

        pagesize = int(req.get('pagesize', 5))
        req.set('pagesize', pagesize)
        pagenumber = int(req.get('pagenumber', 1))
        req.set('pagenumber', pagenumber)

        self.batch = Batch(self.entries,
            pagesize=pagesize, pagenumber=pagenumber, navlistsize=1)

        return self.template()
