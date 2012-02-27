from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import ISitemapView
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from Products.CMFPlone.utils import base_hasattr
from Products.Five import BrowserView
from ftw.blog.interfaces import ICategoryWidget, IBlogUtils
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from zope.component import getMultiAdapter, getUtility
from zope.interface import implements


class SitemapView(BrowserView):
    """ Return a list of all Categories, with the number of blog entries. """

    implements(ISitemapView)

    def createSiteMap(self):
        context = aq_inner(self.context)
        request = context.REQUEST

        fieldName = request.get('fieldName', False)
        uids = request.get('uids', False)

        view = getMultiAdapter((context, self.request),
                               name='category_widget_builder_view')
        data = view.CategoryMap()

        if data is None:
            return None

        # TODO: The recursion should probably be done in python code
        return context.category_widget_edit_view(
            children=data.get('children', []),
            level=0, bottomLevel=0, uids=uids, fieldName=fieldName)


class CategoryWidgetStrategy(SitemapNavtreeStrategy):
    """Use default sitemap strategy
    """

    def decoratorFactory(self, node):
        ct = getToolByName(self.context, 'portal_catalog')
        oldnode = super(CategoryWidgetStrategy, self).decoratorFactory(node)
        oldnode['uid'] = node['item'].UID

        # Determine the number of blog entries for each category.
        # Also take translations of categories into account.
        # TODO: This will perform badly with a large number of categories
        # We could optimize this by always storing a reference to the
        # canonical category instead of the corresponding translation.
        obj = node['item'].getObject()
        count = 0
        if base_hasattr(obj, 'getTranslations'):
            for translation in obj.getTranslations(review_state=False).values():
                count += len(ct(getCategoryUids=translation.UID(),
                                portal_type='BlogEntry',
                                Language='all',))
        else:
            count = len(ct(getCategoryUids=obj.UID(),
                           portal_type='BlogEntry',
                           Language='all',))

        oldnode['count_refs'] = count
        return oldnode


class SiteMapStructure(BrowserView):
    """ Return a FolderTree from the Categories Folder. """

    implements(ICategoryWidget)

    def CategoryMap(self):
        context = aq_inner(self.context)

        query = {}
        query['portal_type'] = ['BlogCategory']

        strategy = getMultiAdapter((context, self), INavtreeStrategy)

        #some modifications for ftw.blog
        strategy.showAllParents = True
        strategy.excludedIds = {}

        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        bloglevel = blogutils.getBlogRoot(context)

        if bloglevel is None:
            return None

        strategy.rootPath = '/'.join(bloglevel.getPhysicalPath()) + \
            '/categories'

        return buildFolderTree(context,
                               obj=context,
                               query=query,
                               strategy=strategy)
