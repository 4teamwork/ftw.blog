from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.blog.interfaces import IBlog, IBlogUtils
from zope.interface import implements


class BlogUtils(object):
    """
    blog utilities
    """
    implements(IBlogUtils)

    def getBlogRoot(self, context):
        obj = context

        while not IPloneSiteRoot.providedBy(obj):
            if IBlog.providedBy(obj):
                return obj
            else:
                obj = aq_parent(aq_inner(obj))

        return None
