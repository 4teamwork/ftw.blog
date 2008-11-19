from zope.interface import implements
from izug.blog.interfaces import IBlog,IBlogUtils
from Acquisition import aq_inner
from zope.component import getMultiAdapter,getUtility
from zope.component import getUtility
from plone.memoize import ram
from Products.CMFCore.utils import getToolByName 
from DateTime import DateTime

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
