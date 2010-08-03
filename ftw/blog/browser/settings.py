from Products.Five.browser import BrowserView
from ftw.blog.interfaces import IBlogUtils
from Acquisition import aq_inner
from zope.component import getMultiAdapter, getUtility


class BlogSettings(BrowserView):
    """show a list of necessarly link for configure a blog"""

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
