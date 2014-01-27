from DateTime import DateTime
from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from ftw.testbrowser.pages import statusmessages
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
import transaction


class TestBlogEntryCollectionPortlet(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.blog = create(Builder('blog').titled('Blog'))

    def add_portlet(self, browser, title=''):
        browser.visit(view='@@manage-portlets')
        browser.forms['form-3'].fill({
            ':action': '/++contextportlets++plone.rightcolumn/+/blog.blogentry'
                       '.collection.portlet'}).submit()

        browser.fill({'Title': title})
        browser.find('Save').click()

    def create_blog_entries(self):
        entry1 = create(Builder('blog entry')
                        .titled('Blog entry 1')
                        .having(test='Just a small text.')
                        .within(self.blog))
        entry2 = create(Builder('blog entry')
                        .titled('Blog entry 2')
                        .having(text='A lot of text. ' * 30)
                        .within(self.blog))

        return entry1, entry2

    @browsing
    def test_portlet_title_is_required(self, browser):
        browser.login()
        self.add_portlet(browser)

        statusmessages.assert_message('There were some errors.')

    @browsing
    def test_default_portlet_creation(self, browser):
        browser.login()
        self.add_portlet(browser, 'Portlet title')

        self.assertTrue(browser.css('body.template-manage-portlets'),
                        'We should be redirected to the manage-portlets view.')

        browser.visit()
        self.assertTrue(browser.css('.portlet.blogentryCollection'),
                        'We created one portlet, but there is none.')

    @browsing
    def test_portlet_edit_view(self, browser):
        browser.login()
        self.add_portlet(browser, 'Portlet title')

        browser.find_link_by_text('BlogEntries collection').click()
        self.assertEquals(plone.first_heading(),
                          'Edit BlogEntry collection portlet',
                          'Wrong title, perhaps we are not on the portlet '
                          'edit view')

        browser.fill({'Title': 'New Title'})
        browser.find('Save').click()

        browser.visit()
        self.assertEquals(
            browser.css(
                '.portlet.blogentryCollection .portletHeader').first.text,
            'New Title',
            'Changing the portlet title did not work.')

    @browsing
    def test_portlet_renderer_result(self, browser):
        entry1, entry2 = self.create_blog_entries()

        browser.login()
        self.add_portlet(browser, 'Portlet title')

        browser.visit()

        titles = browser.css('.blogentryCollection .portletItemTitle').text

        self.assertIn(entry1.Title(), titles, 'Blog title not found')
        self.assertIn(entry2.Title(), titles, 'Blog title not found')

    @browsing
    def test_portlet_renderer_result_order(self, browser):
        entry1, entry2 = self.create_blog_entries()
        entry1.setCreationDate(DateTime('2012-12-12'))
        entry2.setCreationDate(DateTime())
        transaction.commit()

        browser.login()
        self.add_portlet(browser, 'Portlet title')
        ordered_titles = browser.visit().css(
            '.blogentryCollection .portletItemTitle').text

        self.assertEquals([entry2.Title(), entry1.Title()],
                          ordered_titles,
                          'Wrong order.')
