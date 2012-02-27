from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.blog.interfaces import IBlogView, IBlogUtils
from zope.component import getUtility
from zope.interface import implements


class RSSView(BrowserView):
    implements(IBlogView)
    """ Shows a Listing of all Blog entries or
    a RSS listing.

    """

    template=ViewPageTemplateFile("rss.pt")

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

        self.entries = self.context.getFolderContents({
                'sort_on': 'created',
                'sort_order': 'reverse',
                'portal_type': 'BlogEntry'})

        return self.template(self)
