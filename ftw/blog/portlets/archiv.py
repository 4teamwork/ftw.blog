from zope.component import getUtility
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.blog.interfaces import IBlogUtils
from DateTime import DateTime
from Products.CMFPlone.utils import base_hasattr
from zope.i18n import translate
from DateTime.DateTime import _months_a

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

    @property
    def available(self):
        """Only show the portlet, when the blog isn't empty
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        blogroot = blogutils.getBlogRoot(self.context)
        root_path ='/'.join(blogroot.getPhysicalPath())

        all_entries = catalog({'path': root_path,
                              'portal_type': 'BlogEntry'})
        if len(all_entries) > 0:
            return True
        else:
            return False


    def zLocalizedTime(self, time, long_format=False):
        """Convert time to localized time
        """

        month_msgid = 'month_%s' % _months_a[time.strftime("%m")].lower()
        month = translate(month_msgid, domain='plonelocales', context=self.request)
        
        return u"%s %s" % (month, time.strftime('%Y'))

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        blogroot = blogutils.getBlogRoot(self.context)
        if base_hasattr(blogroot, 'getTranslations'):
            blogroots = blogroot.getTranslations(review_state=False).values()
            root_path = ['/'.join(br.getPhysicalPath()) for br in blogroots]
            query['Language'] = 'all'
        else:
            root_path ='/'.join(blogroot.getPhysicalPath())

        query['path'] = root_path
        query['portal_type'] = 'BlogEntry'

        allEntries = catalog(**query)

        values = {}
        for entry in allEntries:
            value = entry.created
            key = value.strftime('%B %Y')
            if not key in values:
                values[key] = value
        values = values.values()
        values.sort(reverse=1)

        infos = []
        for v in values:
            # calc the number of items for the month
            start = DateTime(v.strftime('%Y/%m/01'))
            end = DateTime('%s/%s/%s' % (start.year(), start.month()+ 1, start.day()))
            end = end - 1
            query['created'] = {'query':(start, end), 'range': 'min:max'}
            number = len(catalog(**query))

            infos.append(dict(
                title = self.zLocalizedTime(v),
                number=number,
                url = blogroot.absolute_url()+ \
                    '/view?archiv=' + \
                    v.strftime('%Y/%m/01')))

        self.archivlist = infos

    render = ViewPageTemplateFile('archiv.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
