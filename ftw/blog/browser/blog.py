from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from ftw.blog.interfaces import IBlogView
from plone.app.discussion.interfaces import IConversation
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from urllib import quote_plus
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.interface import implements
from ftw.blog.tools import zLocalizedTime


class BlogView(BrowserView):
    """Shows a Listing of all Blog entries, with the corresponding portlets.
    """

    implements(IBlogView)

    template = ViewPageTemplateFile("blog.pt")
    filters = []

    def __init__(self, *args, **kwargs):
        super(BlogView, self).__init__(*args, **kwargs)
        self.batch = None
        self.entries = None

    def __call__(self):
        """ Get all the Blogentries and return the listingview template.

        It check if the request has some filtering parameters:
        -archive
        -searchable_text
        -getCategoryUids
        -tag
        """

        # TODO: Refactor me. This method is too long!

        context = aq_inner(self.context)
        query = {}
        self.filters = []
        catalog = getToolByName(context, 'portal_catalog')

        if self.request.form.get('archive'):
            datestr = self.request.form.get('archive')
            try:
                start = DateTime(datestr)
            except DateTime.SyntaxError:
                start = DateTime(DateTime().strftime("%Y/%m/01"))
            end = DateTime('%s/%s/%s' % (start.year() + start.month() / 12,
                                         start.month() % 12 + 1, 1))
            end = end - 1
            query['created'] = {'query': (start.earliestTime(),
                                          end.latestTime()),
                                'range': 'minmax'}
            month = zLocalizedTime(self.request, start)
            self.filters.append("%s %s" % (month, start.strftime('%Y')))
        if self.request.form.get('getCategoryUids'):
            uid = self.request.form.get('getCategoryUids')
            category = catalog(UID=uid)[0]
            category_title = category.Title
            if category:
                category_obj = category.getObject()
                if base_hasattr(category_obj, 'getTranslations'):
                    uid = [c.UID() for c in category_obj.getTranslations(
                            review_state=False).values()]
                    translated = category_obj.getTranslation()
                    # If there are no translations getTranslation returns None
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
                aq_parent(context).absolute_url() + querystring)

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

        b_start = self.request.form.get('b_start', 0)
        self.batch = Batch(self.entries, 5, b_start)

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

    def creatorOf(self, item):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(item.Creator)
        if member:
            return {
                'id': member.id,
                'name': member.getProperty('fullname') or member.id}
        return None

    def amount_of_replies(self, brain):
        obj = brain.getObject()
        conversation = IConversation(obj)
        return len([thread for thread in conversation.getThreads()])

    def comments_enabled(self, brain):
        conversation = getMultiAdapter((brain.getObject(), self.request),
                               name='conversation_view')

        return conversation.enabled()
