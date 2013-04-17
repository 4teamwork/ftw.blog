from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.blog.interfaces import IBlogView, IBlogUtils
from zope.component import getUtility
from zope.interface import implements


class RSSView(BrowserView):
    """ Shows a Listing of all Blog entries or
    a RSS listing.

    """

    implements(IBlogView)
    template = ViewPageTemplateFile("rss.pt")

    def __init__(self, *args, **kwargs):
        super(RSSView, self).__init__(*args, **kwargs)
        self.entries = None

    def __call__(self):
        """ Get all the Blogentries

        and  return the standard rss template.

        """
        context = aq_inner(self.context).aq_explicit
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')

        if context.portal_type != 'Blog':
            querystring = context.REQUEST.get('QUERY_STRING', '')
            querystring = querystring and '?' + querystring or querystring
            level = blogutils.getBlogRoot(context)
            url = level.absolute_url() + querystring
            if not self.__name__ == 'rss_blog_view':
                return self.context.REQUEST.RESPONSE.redirect(url)

        query = {
            'sort_on': 'created',
            'sort_order': 'reverse',
            'portal_type': ['BlogEntry', 'SlBlogEntry']
        }
        if 'tag' in self.request.form:
            query['tags'] = self.request.form['tag']
        self.entries = self.context.getFolderContents(query)

        return self.template(self)
