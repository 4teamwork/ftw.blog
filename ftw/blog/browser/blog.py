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

        It check if the request has some filtering parameters:
            -archiv
            -searchable_text
            -getCategoryUids
            -tag
        """

        context = aq_inner(self.context).aq_explicit
        req = context.REQUEST
        query = {}
        self.filters = []
        request = context.REQUEST
        querystring = context.REQUEST.get('QUERY_STRING', '')

        if request.get('archiv'):
            datestr = request.get('archiv')
            start = DateTime(datestr)
            end = DateTime('%s/%s/%s' % (start.year(), start.month()+ 1, start.day()))
            end = end - 1
            query['created'] = {'query': (start, end), 'range': 'min:max'}
            self.filters.append(start.strftime('%B %Y'))
        if request.get('getCategoryUids'):
            uid = request.get('getCategoryUids')
            query['getCategoryUids'] = uid
            category = self.context.portal_catalog(UID=uid)[0]
            self.filters.append(category.Title)
        if request.get('searchable_text'):
            query['SearchableText'] = request.get('searchable_text')
            self.filters.append(query['SearchableText'])
        if request.get('tag'):
            query['tags'] = request.get('tag').decode('utf-8')
            self.filters.append(query['tags'])
        if context.portal_type != 'Blog':
            if querystring:
                querystring = '?%s' % querystring
            return self.context.REQUEST.RESPONSE.redirect(
                aq_parent(aq_inner(self.context)).absolute_url()+ querystring)

        query['sort_on'] = 'created'
        query['sort_order'] = 'reverse'
        query['portal_type'] = 'BlogEntry'
        # show all entries from all languages
        # XXX make this configurable
        translations = self.context.getTranslations().values()
        if not translations:
            self.entries = self.context.getFolderContents(contentFilter=query)
        else:
            paths = ['/'.join(tr[0].getPhysicalPath()) for tr in translations]
            query['path'] = paths
            query['Language'] = 'all'
            self.entries = self.context.portal_catalog(query)

        pagesize = int(req.get('pagesize', 5))
        req.set('pagesize', pagesize)
        pagenumber = int(req.get('pagenumber', 1))
        req.set('pagenumber', pagenumber)

        self.batch = Batch(self.entries,
            pagesize=pagesize, pagenumber=pagenumber, navlistsize=1)

        return self.template()
