from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.blog.portlets.archiv import ArchiveSummary
from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from unittest2 import TestCase


class TestArchiveSummary(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.blog = create(Builder('blog'))

        self.archive_summary = ArchiveSummary(
            self.blog,
            self.request,
            ['ftw.blog.interfaces.IBlogEntry'],
            'created')

    def _create_blog_entry(self, date_str):
        entry = create(Builder('blog entry').within(self.blog))
        entry.setCreationDate(DateTime(date_str))
        entry.reindexObject()

    def test_no_blogs_to_list(self):
        self.assertEquals([], self.archive_summary())

    def test_months_are_sorted_from_newer_to_older(self):
        self._create_blog_entry('2013/01/01')
        self._create_blog_entry('2013/08/01')
        self._create_blog_entry('2013/03/01')

        months = self.archive_summary()[0].get('months')

        self.assertEquals(
            [u'August', u'March', u'January'],
            [month.get('title') for month in months])

    def test_years_are_sorted_from_newer_to_older(self):
        self._create_blog_entry('2011/01/01')
        self._create_blog_entry('2015/08/01')
        self._create_blog_entry('2013/03/01')

        result = self.archive_summary()

        self.assertEquals(
            ['2015', '2013', '2011'],
            [year.get('title') for year in result])

    def test_count_all_blog_entries_for_each_year_in_the_title(self):
        self._create_blog_entry('2011/01/01')
        self._create_blog_entry('2011/08/01')
        self._create_blog_entry('2011/03/01')
        self._create_blog_entry('2012/03/01')
        self._create_blog_entry('2012/08/01')

        result = self.archive_summary()

        self.assertEquals(
            [2, 3],
            [year.get('number') for year in result])

    def test_count_all_blog_entries_for_each_month(self):
        self._create_blog_entry('2013/01/01')
        self._create_blog_entry('2013/01/04')
        self._create_blog_entry('2013/01/06')
        self._create_blog_entry('2013/02/06')
        self._create_blog_entry('2013/02/04')
        self._create_blog_entry('2012/02/04')

        result = self.archive_summary()

        months_2013 = result[0].get('months')
        months_2012 = result[1].get('months')

        self.assertEquals(
            [2, 3],
            [month.get('number') for month in months_2013])

        self.assertEquals(
            [1],
            [month.get('number') for month in months_2012])
