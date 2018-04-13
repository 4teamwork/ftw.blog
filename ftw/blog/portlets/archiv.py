from DateTime import DateTime
from ftw.blog.interfaces import IBlogUtils
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from zope.interface import implements
from ftw.blog.tools import zLocalizedTime


class IArchivePortlet(IPortletDataProvider):
    """Archive portlet interface.
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
        return bool(self.archive_summary())

    @memoize
    def archive_summary(self):
        """Returns an ordered list of summary infos per month."""
        blogutils = getUtility(IBlogUtils, name='ftw.blog.utils')
        blogroot = blogutils.getBlogRoot(self.context)

        return ArchiveSummary(
            blogroot,
            self.request,
            ['ftw.blog.interfaces.IBlogEntry'],
            'created')()

    render = ViewPageTemplateFile('archiv.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()


class ArchiveSummary(object):

    def __init__(self, context, request, interfaces, datefield, viewname=None):
        self.context = context
        self.request = request
        self.interfaces = interfaces
        self.datefield = datefield
        self.viewname = viewname
        self.selected_year = None
        self.selected_month = None

    def __call__(self):
        self._set_selected_archive()

        entries = self._get_archive_entries()
        counter = self._count_entries(entries)

        result = []
        year_numbers = sorted(counter, reverse=True)

        for year_number in year_numbers:

            year = counter.get(year_number)
            months = year.get('months')
            month_numbers = sorted(months, reverse=True)
            month_list = []

            for month_number in month_numbers:
                date = '%s/%s/01' % (year_number, month_number)

                month_list.append(dict(
                    title=zLocalizedTime(self.request, DateTime(date)),
                    number=months.get(month_number),
                    url=self._get_archive_url(date),
                    mark=[self.selected_year, self.selected_month] == [
                        year_number, month_number]
                ))

            result.append(dict(
                title=year_number,
                number=year.get('num'),
                months=month_list,
                mark=self.selected_year == year_number
            ))

        return result

    def _set_selected_archive(self):
        selected_archive = self.request.get('archive')
        if selected_archive:
            self.selected_year = selected_archive.split('/')[0]
            self.selected_month = selected_archive.split('/')[1]

    def _get_archive_url(self, date):
        if self.viewname:
            return '%s/%s?archive=%s' % (
                self.context.absolute_url(),
                self.viewname,
                date)
        else:
            return '%s?archive=%s' % (self.context.absolute_url(), date)

    def _get_archive_entries(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(**self._get_query())

    def _get_query(self):
        query = {}
        if base_hasattr(self.context, 'getTranslations'):
            roots = self.context.getTranslations(
                review_state=False).values()
            root_path = ['/'.join(br.getPhysicalPath()) for br in roots]
            query['Language'] = 'all'
        else:
            root_path = '/'.join(self.context.getPhysicalPath())

        query['path'] = root_path
        query['object_provides'] = self.interfaces

        return query

    def _count_entries(self, entries):
        """Return a summary map like:

        {'2009': {
            'num': 6,
            'months': {
                '01': 4,
                '02': 2}
            }
        }
        """
        summary = {}

        for entry in entries:

            date = getattr(entry, self.datefield)
            if not date:
                continue

            if date.year() <= 1900:
                continue

            year_name = date.strftime('%Y')
            month_name = date.strftime('%m')

            year_summary = summary.get(year_name, {})
            month_summary = year_summary.get('months', {})

            # Increase month
            month_summary.update(
                {month_name: month_summary.get(month_name, 0) + 1})
            year_summary.update({'months': month_summary})

            # Increase year
            year_summary.update({'num': year_summary.get('num', 0) + 1})
            summary.update({year_name: year_summary})

        return summary
