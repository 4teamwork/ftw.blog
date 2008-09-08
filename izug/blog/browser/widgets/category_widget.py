from Acquisition import aq_inner
from zope.component import getMultiAdapter,getUtility
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from Products.CMFPlone.browser.interfaces import ISitemapView

from izug.blog.interfaces import ICategoryWidget, IBlog, IBlogUtils


from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree

class SitemapView(BrowserView):
    implements(ISitemapView)

    def createSiteMap(self):
        context = aq_inner(self.context)
        request = context.REQUEST
        
        fieldName = request.get('fieldName',False)
        uids = request.get('uids',False)
        
        view = getMultiAdapter((context, self.request),
                               name='category_widget_builder_view')
        data = view.CategoryMap()

        #properties = getToolByName(context, 'portal_properties')
        #navtree_properties = getattr(properties, 'navtree_properties')
        #bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        # XXX: The recursion should probably be done in python code
        return context.category_widget_edit_view(children=data.get('children',[]),
                                             level=0, bottomLevel=0,uids=uids,fieldName=fieldName)
                     
                                             
class CategoryWidgetStrategy(SitemapNavtreeStrategy):
    """
    use default sitemap strategy
    """
    def decoratorFactory(self, node):
        rc = getToolByName(self.context,'portal_catalog')
        oldnode = super(CategoryWidgetStrategy, self).decoratorFactory(node)
        oldnode['uid'] = node['item'].UID
        oldnode['count_refs'] = len(rc({'portal_type':'Blog Entry','getCategoryUids': oldnode['uid']}))
        return oldnode 

class SiteMapStructure(BrowserView):
    implements(ICategoryWidget)

    def CategoryMap(self):
        context = aq_inner(self.context)

        #build the simple query
        query = {}
        query['portal_type'] = ['Blog Category']

        strategy = getMultiAdapter((context, self), INavtreeStrategy)
        
        #some modifications for Izug.blog
        strategy.showAllParents = True
        strategy.excludedIds = {}
        
        blogutils = getUtility(IBlogUtils,name='izug.blog.utils')
        bloglevel = blogutils.getBlogRoot(context)
            
            
        strategy.rootPath = '/'.join(bloglevel.getPhysicalPath()) + '/categories'

        return buildFolderTree(context, obj=context, query=query, strategy=strategy)
