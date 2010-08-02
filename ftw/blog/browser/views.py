from Products.Five.browser import BrowserView
from zope.interface import implements
from ftw.blog.interfaces import IBlogView, IBlogEntryView, IBlogUtils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.content.batching import Batch
from Acquisition import aq_inner
from zope.component import getMultiAdapter, getUtility


class BlogEntryView(BrowserView):
    implements(IBlogEntryView)
    template=ViewPageTemplateFile("blog_entry_view.pt")

    def __call__(self):
        #context.REQUEST.set('disable_border',1)
        return self.template()


class BlogView(BrowserView):
    implements(IBlogView)
    """
    Uses default plone folder_listing.pt as base
    nearly everything is in the template.
    It works with Topics too
    """
    template=ViewPageTemplateFile("blog_view.pt")

    batching=ViewPageTemplateFile("batching.pt")

    def __call__(self):
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        context = aq_inner(self.context).aq_explicit
        req = context.REQUEST
        querystring = context.REQUEST.get('QUERY_STRING', '')
        querystring = querystring and '?' + querystring or querystring

        if context.Type() == 'Collection':
            """
            do nothing
            """

        elif context.Type() == 'Blog':
            pagesize = int(req.get('pagesize', 5))
            req.set('pagesize', pagesize)
            pagenumber = int(req.get('pagenumber', 1))
            req.set('pagenumber', pagenumber)

            self.entries = self.context.getFolderContents({
                'sort_on': 'created',
                'sort_order': 'reverse',
                'portal_type': 'BlogEntry'})

            self.batch = Batch(self.entries,
                               pagesize=pagesize,
                               pagenumber=pagenumber,
                               navlistsize=1)

        else:

            level = blogutils.getBlogRoot(context)

            url = level.absolute_url() + querystring
            if not self.__name__ == 'rss_blog_view':
                self.context.REQUEST.RESPONSE.redirect(url)
            else:
                url = level.absolute_url() + '/rss_blog_view' + querystring
                self.context.REQUEST.RESPONSE.redirect(url)

        if self.__name__ == 'rss_blog_view':
            self.template=ViewPageTemplateFile("rss_blog_view.pt")
            return self.template()

        return self.template()


class createBlogEntryPath(BrowserView):

    def URL(self):
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        level = blogutils.getBlogRoot(self.context)
        return '%s/createObject?type_name=Blog+Entry' % level.absolute_url()


class BlogSettings(BrowserView):

    def getBlog(self, context):
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        return blogutils.getBlogRoot(context)

    def objectActions(self):
        context = aq_inner(self.context)
        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        return context_state.actions().get('object_blog_settings_actions', [])

    def managePortletUrl(self):
        level = self.getBlog(self.context)

        return '%s/@@manage-blog-portlets' % level.absolute_url()

    def editBlog(self):
        level = self.getBlog(self.context)
        return '%s/edit' % level.absolute_url()
