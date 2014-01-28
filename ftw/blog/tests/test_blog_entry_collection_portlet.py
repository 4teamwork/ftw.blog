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
from StringIO import StringIO
from unittest2 import TestCase
import transaction


class TestBlogEntryCollectionPortlet(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.blog = create(Builder('blog').titled('Blog'))

    def add_portlet(self, browser, **kwargs):
        browser.visit(view='@@manage-portlets')
        browser.forms['form-3'].fill({
            ':action': '/++contextportlets++plone.rightcolumn/+/blog.blogentry'
                       '.collection.portlet'}).submit()

        browser.fill(kwargs)
        browser.find('Save').click()

    def create_blog_entries(self):
        image = StringIO(
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')

        entry1 = create(Builder('blog entry')
                        .titled('Blog entry 1')
                        .having(text='Just a small text.',
                                leadimage=image)
                        .within(self.blog))
        entry2 = create(Builder('blog entry')
                        .titled('Blog entry 2')
                        .having(text='A lot of text. ' * 30,
                                leadimage=image)
                        .within(self.blog))

        return entry1, entry2

    @browsing
    def test_portlet_title_is_required(self, browser):
        browser.login()
        self.add_portlet(browser, **{'Title': ''})

        statusmessages.assert_message('There were some errors.')

    @browsing
    def test_default_portlet_creation(self, browser):
        self.create_blog_entries()
        browser.login()
        self.add_portlet(browser, **{'Title': 'Portlet title'})

        self.assertTrue(browser.css('body.template-manage-portlets'),
                        'We should be redirected to the manage-portlets view.')

        browser.visit()
        self.assertTrue(browser.css('.portlet.blogentryCollection'),
                        'We created one portlet, but there is none.')

    @browsing
    def test_portlet_edit_view(self, browser):
        self.create_blog_entries()
        browser.login()
        self.add_portlet(browser, **{'Title': 'Portlet title'})

        browser.find_link_by_text('BlogEntries collection portlet').click()
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
        self.add_portlet(browser, **{'Title': 'Portlet title'})

        titles = browser.visit().css(
            '.blogentryCollection .portletItemTitle').text

        self.assertIn(entry1.Title(), titles, 'Blog title not found')
        self.assertIn(entry2.Title(), titles, 'Blog title not found')

    @browsing
    def test_portlet_renderer_result_order(self, browser):
        entry1, entry2 = self.create_blog_entries()
        entry1.setCreationDate(DateTime('2012-12-12'))
        entry1.reindexObject()
        transaction.commit()

        browser.login()
        self.add_portlet(browser, **{'Title': 'Portlet title'})
        ordered_titles = browser.visit().css(
            '.blogentryCollection .portletItemTitle').text

        self.assertEquals([entry2.Title(), entry1.Title()],
                          ordered_titles,
                          'Wrong order.')

    @browsing
    def test_portlet_renderer_crop_description(self, browser):
        entry1, entry2 = self.create_blog_entries()
        transaction.commit()
        browser.login()
        info = {'Title': 'Portlet title', 'Show description': True}
        self.add_portlet(browser, **info)
        descriptions = browser.visit().css(
        '.blogentryCollection .portletItemDescription').text

        self.assertEquals(2, len(descriptions), 'Expect two items')

        self.assertLessEqual(
            len(descriptions[1]),
            200 + 3,  # max 200 plus 3 dots
            'Description not cropped')

    @browsing
    def test_portlet_renderer_do_not_show_description(self, browser):
        entry1, entry2 = self.create_blog_entries()
        browser.login()
        info = {'Title': 'Portlet title', 'Show description': False}
        self.add_portlet(browser, **info)

        self.assertFalse(
            len(browser.visit().css(
                '.blogentryCollection .portletItemDescription')),
            'There should be no description displayed.')

    @browsing
    def test_portlet_renderer_include_path_query(self, browser):
        entry1, entry2 = self.create_blog_entries()
        blog2 = create(Builder('blog').titled('Second blog'))
        entry3 = create(Builder('blog entry')
            .within(blog2)
            .titled('Third entry'))

        browser.login()
        info = {'Title': 'Portlet title',
                'Blogs': ['/'.join(blog2.getPhysicalPath())]}
        self.add_portlet(browser, **info)

        items = browser.visit().css(
            '.blogentryCollection .portletItemTitle').text
        self.assertEquals(1, len(items), 'Expect one entry.')

        self.assertEquals(entry3.Title(), items[0])

    @browsing
    def test_portlet_renderer_availability(self, browser):
        browser.login()
        info = {'Title': 'Portlet title'}
        self.add_portlet(browser, **info)

        self.assertFalse(len(browser.css('.blogentryCollection')),
                         'There should be no portlet available.')

    @browsing
    def test_portlet_renderer_result_quantity(self, browser):
        entry1, entry2 = self.create_blog_entries()
        browser.login()
        info = {'Title': 'Portlet title', 'Quantity': '1'}
        self.add_portlet(browser, **info)

        self.assertEquals(
            1,
            len(browser.visit().css('.blogentryCollection .portletItemTitle')),
            'There should be one entry.')

    @browsing
    def test_portlet_renderer_show_images(self, browser):
        entry1, entry2 = self.create_blog_entries()

        browser.login()
        info = {'Title': 'Portlet title', 'Show leadimages': True}
        self.add_portlet(browser, **info)

        self.assertEquals(
            2,
            len(browser.visit().css('.blogentryCollection .portletItemImage')),
            'Expect 2 entries with 2 images.')

    @browsing
    def test_portlet_renderer_do_NOT_show_images(self, browser):
        entry1, entry2 = self.create_blog_entries()

        browser.login()
        info = {'Title': 'Portlet title', 'Show leadimages': False}
        self.add_portlet(browser, **info)

        self.assertEquals(
            0,
            len(browser.visit().css('.blogentryCollection .portletItemImage')),
            'Expect 2 entries with 0 images.')
