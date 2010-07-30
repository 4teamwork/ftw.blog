from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.comments import CommentsViewlet
from ftw.blog.interfaces import IBlogUtils
from ftw.blog import _


class FtwBlogActionsBar(ViewletBase):

    render = ViewPageTemplateFile('ftw_blog_actionsbar.pt')


class FtwBlogNavigation(ViewletBase):

    render = ViewPageTemplateFile('ftw_blog_navigation.pt')

    def update(self):
        context = aq_inner(self.context)
        parent = context.aq_parent
        catalog = getToolByName(context, 'portal_catalog')
        query = {}
        query['portal_type'] = 'BlogEntry'
        query['sort_on'] = 'created'
        query['path'] = '/'.join(parent.getPhysicalPath())
        results = catalog(query)

        uids = [b.UID for b in results]
        current_uid = context.UID()
        current_index = uids.index(current_uid)
        # we have to convert the new indexes to strings,
        # otherwhise this two lines blow will no work correctly
        prev_index = current_index != 0 and str(current_index - 1) or False
        next_index = current_index != len(uids)-1 \
                        and str(current_index+1) or False

        if prev_index:
            prev = dict(title=self.cropTitle(results[int(prev_index)].Title),
                        url = results[int(prev_index)].getURL())
        if next_index:
            next = dict(title=self.cropTitle(results[int(next_index)].Title),
                        url = results[int(next_index)].getURL())
        self.prev = prev_index and prev
        self.next = next_index and next

    def cropTitle(self, title):
        return len(title) > 20 and title[:20] + '... ' or title


class FtwBlogListNavigation(ViewletBase):

    render = ViewPageTemplateFile('ftw_blog_navigation.pt')

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        bloglevel = blogutils.getBlogRoot(self.context)

        category = self.context.REQUEST.get('getCategoryUids', '')
        tags = self.context.REQUEST.get('tags', '')
        archiv = self.context.REQUEST.get('InfosForArchiv', '')
        extend_querystring = category and \
                                '&getCategoryUids=%s' % category or ''
        extend_querystring += tags and '&tags=%s' % tags or ''
        extend_querystring += archiv and '&InfosForArchiv=%s' % archiv or ''

        query = {}
        query['portal_type'] = 'BlogEntry'
        query['getCategoryUids'] = category
        query['tags'] = tags
        query['InfosForArchiv'] = archiv
        query['path'] = '/'.join(bloglevel.getPhysicalPath())
        allItems = len(catalog(query))

        b_start = int(self.context.REQUEST.get('b_start', 0))
        b_size = int(self.context.REQUEST.get('b_size', 5))
        b_size = aq_inner(self.context).Type() == 'Collection' \
                        and int(self.context.getItemCount()) or b_size

        b_diff_prev = b_start + b_size
        b_diff_next = b_start - b_size

        if b_diff_prev >= allItems:
            prev_url = False
        else:
            querystring_prev = '?b_start=%s' % b_diff_prev
            prev_url = aq_inner(self.context).absolute_url() +\
                        querystring_prev +\
                        extend_querystring

        self.prev = prev_url and dict(title=_(u'Old entries'),
                                      url=prev_url) or False

        if b_diff_next < 0:
            next_url = False
        else:
            querystring_next = '?b_start=%s' % b_diff_next
            next_url = aq_inner(self.context).absolute_url() +\
                        querystring_next +\
                        extend_querystring

        self.next = next_url and dict(title=_(u'New entries'),
                                      url=next_url) or False


class CommentsViewlet(CommentsViewlet):
    render = ViewPageTemplateFile('ftw_comments.pt')
