from Acquisition import aq_inner
from Products.CMFPlone.browser.interfaces import ISitemapView
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.blog.interfaces import IBlogUtils
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter, getUtility
from zope.interface import implements


class ICategoriesPortlet(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(ICategoriesPortlet)

    @property
    def title(self):
        return "Blog Categories Portlet"


class Renderer(base.Renderer):

    def __init__(self, *args, **kwargs):
        super(Renderer, self).__init__(*args, **kwargs)
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        self.root = blogutils.getBlogRoot(self.context)

    @property
    def available(self):
        if not self.root:
            return False

        categories = getattr(self.root, 'categories', None)
        if not categories or not getattr(categories, 'objectIds', None):
            return False

        if not categories.objectIds():
            return False

        return True

    def update(self):
        if self.root:
            self.blogroot = self.root.absolute_url()
        else:
            self.blogroot = ''

    render = ViewPageTemplateFile('categories.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()


class CategoryPortletSitemapView(BrowserView):
    implements(ISitemapView)

    def createSiteMap(self):
        context = aq_inner(self.context)

        view = getMultiAdapter((context, self.request),
                               name='category_widget_builder_view')
        data = view.CategoryMap()

        #properties = getToolByName(context, 'portal_properties')
        #navtree_properties = getattr(properties, 'navtree_properties')
        #bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        # XXX: The recursion should probably be done in python code
        return context.category_portlet_recurs_view(
            children=data.get('children', []),
            level=0, bottomLevel=0)
