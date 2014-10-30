from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import transaction
from unittest2 import TestCase

from ftw.blog.interfaces import IBlog
from ftw.blog.interfaces import IBlogEntry
from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING


class TestContentTypeCreation(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        transaction.commit()

    @browsing
    def test_create_blog(self, browser):
        browser.login().visit()

        factoriesmenu.add('Blog')
        browser.fill({'Title': 'Blogu'}).submit()

        blog = self.portal.get('blogu')
        self.assertTrue(IBlog.providedBy(blog))

    @browsing
    def test_create_blog_entry(self, browser):
        browser.login().visit()

        factoriesmenu.add('Blog')
        browser.fill({'Title': 'Blogu'}).submit()

        factoriesmenu.add('Blog entry')
        browser.fill({'Title': 'Hello World'})
        browser.find_button_by_label('Save').click()

        blog_entry = self.portal.get('blogu').get('hello-world')
        self.assertTrue(IBlogEntry.providedBy(blog_entry))
