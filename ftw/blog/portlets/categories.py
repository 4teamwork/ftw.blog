from zope.interface import implements
from Acquisition import aq_inner
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five import BrowserView

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from Products.CMFPlone.browser.interfaces import ISitemapView
from ftw.blog.interfaces import IBlogUtils

class ICategoriesPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    implements(ICategoriesPortlet)
    @property
    def title(self):
        return "Blog Categories Portlet"

class Renderer(base.Renderer):

    def update(self):
        blogutils = getUtility(IBlogUtils,name='ftw.blog.utils')
        blogroot = blogutils.getBlogRoot(self.context)
        
        if blogroot:
            self.blogroot = blogroot.absolute_url()
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
        request = context.REQUEST
               
        #IMPORTANT use category widget builder!
        view = getMultiAdapter((context, self.request),
                               name='category_widget_builder_view')
        data = view.CategoryMap()

        #properties = getToolByName(context, 'portal_properties')
        #navtree_properties = getattr(properties, 'navtree_properties')
        #bottomLevel = navtree_properties.getProperty('bottomLevel', 0)
        # XXX: The recursion should probably be done in python code
        return context.category_portlet_recurs_view(children=data.get('children',[]),
                                             level=0, bottomLevel=0)
                                             
                                             
                                             
                                             
