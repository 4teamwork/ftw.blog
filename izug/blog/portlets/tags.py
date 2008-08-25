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
from Products.CMFPlone.browser.interfaces import ISitemapView

from izug.blog import blogMessageFactory as _

class ITagsPortlet(IPortletDataProvider):

    maxsize = schema.ASCIILine(title=_(u'Max. Fontsize'),
                       description=_(u'Size in em'),
                       required=True,
                       default='2em')

    minsize = schema.ASCIILine(title=_(u'Min. Fontsize'),
                       description=_(u'Size in em'),
                       required=True,
                       default='0.7em')

class Assignment(base.Assignment):
    implements(ITagsPortlet)
    
    def __init__(self, maxsize='2em',minsize='0.7em'):
        self.maxsize = maxsize
        self.minsize = minsize

    @property
    def title(self):
        return "Blog Tags Portlet"

class Renderer(base.Renderer):
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data

        catalog = getToolByName(self.context,'portal_catalog')
        alltags = catalog.uniqueValuesFor("getTags")
        query = {}
        query['portal_type'] = 'Blog Entry'

        weightlist = []
        for tag in alltags:
            query['getTags'] = tag
            count = len(catalog(query))
            weightlist.append(count)
        weightlist.sort()
        
        if weightlist:
            minimal = weightlist[:1][0]
            maximal = weightlist[-1:][0]
            
            maxsize = float(self.data.maxsize)
            minsize = float(self.data.minsize)
           
            tagclouds = []
            for tag in alltags:
                query['getTags'] = tag
                numberofblogs = len(catalog(query))
                
                #calc tagclouds --> http://de.wikipedia.org/wiki/TagCloud
                size = float((maxsize*(numberofblogs-minimal)))/float((maximal-minimal))
                
                if numberofblogs <= minimal or size < minsize:
                    size = float(self.data.minsize)
                
                info = dict(title=tag,
                            fontsize=round(size,1))
                tagclouds.append(info)
            
            tagclouds.sort(lambda x, y: cmp(x['title'], y['title']))
            self.tagclouds = tagclouds
        else:
            self.tagclouds = []
       
        
    render = ViewPageTemplateFile('tags.pt')

class AddForm(base.AddForm):
    form_fields = form.Fields(ITagsPortlet)
    label = _(u"Add TagCloud Portlet")
    description = _(u"This portlet displays the TagCloud from izug.blog")

    def create(self, data):
        return Assignment(maxsize=data.get('maxsize', '2em'),
                          minsize=data.get('minsize', '0.7em'))

class EditForm(base.EditForm):
    form_fields = form.Fields(ITagsPortlet)
    label = _(u"Edit Tag Portlet")
    description = _(u"This portlet displays the TagCloud from izug.blog")
