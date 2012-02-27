from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.blog.interfaces import IBlogUtils
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implements


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
        if self.archive_summary():
            return True
        else:
            return False

    def zLocalizedTime(self, time, long_format=False):
        """Convert time to localized time
        """
        month_msgid = 'month_%s' % time.strftime("%b").lower()
        month = translate(month_msgid, domain='plonelocales', context=self.request)

        return u"%s %s" % (month, time.strftime('%Y'))

    @memoize
    def archive_summary(self):
        """Returns an ordered list of summary infos per month."""
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

        archive_counts = {}
        blog_entries = catalog(**query)
        for entry in blog_entries:
            year_month = entry.created.strftime('%Y/%m')
            if year_month in archive_counts:
                archive_counts[year_month] += 1
            else:
                archive_counts[year_month] = 1

        archive_summary = []
        ac_keys = archive_counts.keys()
        ac_keys.sort(reverse=True)
        for year_month in ac_keys:
            archive_summary.append(dict(
                title=self.zLocalizedTime(DateTime('%s/01' % year_month)),
                number=archive_counts[year_month],
                url='%s?archiv=%s/01' % (blogroot.absolute_url(), year_month),
            ))
        return archive_summary

    render = ViewPageTemplateFile('archiv.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
