from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from unittest2 import TestCase
from pyquery import PyQuery
from StringIO import StringIO
import transaction


class TestBlogEntry(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestBlogEntry, self).setUp()

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        blog = self.portal.get(self.portal.invokeFactory('Blog', 'blog'))
        self.entry = blog.get(
            blog.invokeFactory('BlogEntry', 'entry', title="Entry"))

        image = StringIO(
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')

        self.entry.invokeFactory('Image', 'image', title='Image',
                                 file=image)

        transaction.commit()

    def test_show_images(self):
        self.browser.open(self.entry.absolute_url())
        doc = PyQuery(self.browser.contents)
        self.assertEquals(len(doc('.blogImages img')), 1, 'Expect one image')

    def test_do_not_show_images(self):
        self.entry.setShowImages(False)
        transaction.commit()
        self.browser.open(self.entry.absolute_url())
        doc = PyQuery(self.browser.contents)
        self.assertEquals(len(doc('.blogImages img')), 0,
                          'Expect no image')
