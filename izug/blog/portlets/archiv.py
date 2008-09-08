from zope.interface import implements
from Acquisition import aq_inner
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from izug.blog.interfaces import IBlogUtils
from DateTime import DateTime

class IArchivePortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    implements(IArchivePortlet)
    @property
    def title(self):
        return "Blog Archive Portlet"

class Renderer(base.Renderer):
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data


    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        values = list(catalog.uniqueValuesFor('InfosForArchiv'))
        values.sort()
        
        infos = []
        for v in values:
            infos.append(dict(title = DateTime(v).strftime('%B %Y'),
                              url = self.context.absolute_url()+'/blog_view?InfosForArchiv=' + v
                              )
                        )
            
        self.archivlist = infos
    
        
    render = ViewPageTemplateFile('archiv.pt')


class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()

