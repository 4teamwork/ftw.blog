from zope.interface import implements
from Acquisition import aq_inner
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
from izug.blog.interfaces import IBlogUtils, IArchivable
from DateTime import DateTime

MONTHS_GER = {
			'01':u'Januar',
			'02':u'Februar',
			'03':unicode('M\xc3\xa4arz','utf-8'),
			'04':u'April',
			'05':u'Mai',
			'06':u'Juni',
			'07':u'Juli',
			'08':u'August',
			'09':u'September',
			'10':u'Oktober',
			'11':u'November',
			'12':u'Dezember',	
}

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
        self.request = request
        self._translation_service = getToolByName(context, 'translation_service')

    def zLocalizedTime(self, time, long_format=False):
        """Convert time to localized time
        """
        context = aq_inner(self.context) 
        return u"%s %s" % (MONTHS_GER[time.strftime("%m")], time.strftime('%Y'))

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        blogutils = getUtility(IBlogUtils,name='izug.blog.utils')
        blogroot =  blogutils.getBlogRoot(self.context)
        root_path ='/'.join(blogroot.getPhysicalPath())
        
        allEntries = catalog({'path' : root_path,
                              'object_provides' : IArchivable.__identifier__})
                              
        values = {}
        for entry in allEntries:
            value = entry.created
            key = value.strftime('%B %Y')
            if not values.has_key(key):
                values[key] = value
        values = values.values()
        values.sort(reverse=1)
        
        infos = []
        for v in values:
            infos.append(dict(title = self.zLocalizedTime(v),
                              url = self.context.absolute_url()+'/view?InfosForArchiv=' + v.strftime('%m/01/%Y')
                              )
                        )
            
        self.archivlist = infos
    
        
    render = ViewPageTemplateFile('archiv.pt')


class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()

