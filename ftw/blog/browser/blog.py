from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.blog.interfaces import IBlogView
from plone.app.content.batching import Batch
from urllib import quote_plus
from zope.i18n import translate
from zope.interface import implements


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

        context = aq_inner(self.context)
        query = {}
        self.filters = []
        catalog = getToolByName(context, 'portal_catalog')

        if self.request.form.get('archiv'):
            datestr = self.request.form.get('archiv')
            try:
                start = DateTime(datestr)
            except DateTime.SyntaxError:
                start = DateTime(DateTime().strftime("%Y/%m/01"))
            end = DateTime('%s/%s/%s' % (start.year() + start.month() / 12,
                                         start.month() % 12 + 1, 1))
            end = end - 1
            query['created'] = {'query': (start.earliestTime(), end.latestTime()), 'range': 'minmax'}
            month_msgid = 'month_%s' % start.strftime("%b").lower()
            month = translate(month_msgid, domain='plonelocales', context=self.request)
            self.filters.append("%s %s" % (month, start.strftime('%Y')))
        if self.request.form.get('getCategoryUids'):
            uid = self.request.form.get('getCategoryUids')
            category = catalog(UID=uid)[0]
            category_title = category.Title
            if category:
                category_obj = category.getObject()
                if base_hasattr(category_obj, 'getTranslations'):
                    uid = [c.UID() for c in category_obj.getTranslations(review_state=False).values()]
                    translated = category_obj.getTranslation()
                    # If there are no translations, getTranslation returns 'None'
                    if translated:
                        category_title = translated.Title()
            query['getCategoryUids'] = uid
            category = catalog(UID=uid)[0]
            self.filters.append(category_title)
        if self.request.form.get('searchable_text'):
            query['SearchableText'] = self.request.get('searchable_text')
            self.filters.append(query['SearchableText'])
        if self.request.form.get('tag'):
            query['tags'] = self.request.form.get('tag').decode('utf-8')
            self.filters.append(query['tags'])
        if context.portal_type != 'Blog':
            querystring = self.query_string()
            if querystring:
                querystring = '?%s' % querystring
            return self.request.response.redirect(
                aq_parent(context).absolute_url()+ querystring)

        query['sort_on'] = 'created'
        query['sort_order'] = 'reverse'
        query['portal_type'] = 'BlogEntry'
        # show all entries from all languages
        # XXX make this configurable
        if not base_hasattr(context, 'getTranslations'):
            self.entries = context.getFolderContents(contentFilter=query)
        else:
            translations = context.getTranslations().values()
            paths = ['/'.join(tr[0].getPhysicalPath()) for tr in translations]
            query['path'] = paths
            query['Language'] = 'all'
            self.entries = catalog(query)

        pagesize = int(self.request.form.get('pagesize', 5))
        #req.set('pagesize', pagesize)
        pagenumber = int(self.request.form.get('pagenumber', 1))
        #req.set('pagenumber', pagenumber)

        self.batch = Batch(self.entries,
                           pagesize=pagesize, pagenumber=pagenumber, navlistsize=1)

        return self.template()


    def query_string(self, **args):
        """Updates the query string of the current request with the given
        keyword arguments and returns it as a quoted string.
        """
        query = self.request.form.copy()
        # Remove empty query parameters
        for k, v in query.items():
            if v == '':
                del query[k]
        query.update(args)
        return '&'.join(["%s=%s" % (quote_plus(str(k)), quote_plus(str(v)))
                         for k, v in query.items()])
