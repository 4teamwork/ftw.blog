from zope.interface import implements
from izug.blog.interfaces import IBlog,IBlogUtils
from Acquisition import aq_inner
from zope.component import getMultiAdapter,getUtility
from zope.component import getUtility
from plone.memoize import ram
from Products.CMFCore.utils import getToolByName 
from DateTime import DateTime
import logging
logger = logging.getLogger('blogutils')


def blogRootCacheKey(fun, self, context):
    hour = DateTime().hour()
    cachekey = "%s%s" % (context.UID(),hour)
    return hash(cachekey)


class BlogUtils(object):
    """
    blog utilities
    """
    implements(IBlogUtils)
    
    @ram.cache(blogRootCacheKey)
    def getBlogRoot(self,context):
        level = aq_inner(context).aq_explicit
        while not IBlog.providedBy(level):
            level = level.aq_parent

        logger.info('utils function is no cached')
        return level
