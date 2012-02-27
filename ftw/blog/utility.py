from zope.interface import implements
from ftw.blog.interfaces import IBlog,IBlogUtils
from Acquisition import aq_inner
from zope.component import getMultiAdapter


class BlogUtils(object):
    """
    blog utilities
    """
    implements(IBlogUtils)

    def getBlogRoot(self,context):
        level = aq_inner(context).aq_explicit
        portal_state = getMultiAdapter((context, context.REQUEST), name=u'plone_portal_state')
        portal_root = portal_state.portal()
        while not IBlog.providedBy(level):
            if level == portal_root:
                return None
            level = level.aq_parent
        return level
