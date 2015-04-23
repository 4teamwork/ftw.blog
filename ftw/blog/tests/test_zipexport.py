from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from unittest2 import TestCase
from zipfile import ZipFile
from StringIO import StringIO


class TestBlogZipexport(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.blog = create(Builder('blog').titled('The Blog'))
        create(Builder('blog entry').titled('First Chapter')
               .within(self.blog))
        create(Builder('blog entry').titled('The SubChapter')
               .within(self.blog))

    @browsing
    def test_zipexport_integration(self, browser):
        browser.login().visit(self.blog, view='zip_export')

        self.assertEquals('application/zip', browser.headers['Content-Type'])

        zipfile = ZipFile(StringIO(browser.contents))
        self.assertEquals(['the-blog.pdf'], zipfile.namelist())
