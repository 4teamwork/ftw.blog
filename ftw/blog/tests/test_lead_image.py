from ftw.blog.interfaces import IBlogSettings
from ftw.blog.testing import FTW_BLOG_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from pyquery import PyQuery
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import getUtility


class TestLeadImage(TestCase):

    layer = FTW_BLOG_INTEGRATION_TESTING

    def setUp(self):
        super(TestLeadImage, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        blog = self.portal.get(self.portal.invokeFactory('Blog', 'blog'))
        self.entry = blog.get(blog.invokeFactory('BlogEntry', 'entry'))

    def enable_lead_image(self):
        registry = getUtility(IRegistry)
        registry.forInterface(IBlogSettings).blog_entry_has_lead_image = True

    def test_blog_entry_has_no_lead_image_by_default(self):

        field = self.entry.Schema()['leadimage']
        self.assertFalse(
            field.widget.testCondition(None, self.portal, self.entry))

    def test_blog_entry_has_lead_image(self):
        self.enable_lead_image()

        field = self.entry.Schema()['leadimage']
        self.assertTrue(
            field.widget.testCondition(None, self.portal, self.entry))

    def test_do_not_show_image_on_entry_view(self):
        view = self.entry.restrictedTraverse('@@blog_entry_view')

        self.assertFalse(view.show_lead_image())

        self.enable_lead_image()
        # Still false, because there is no image
        self.assertFalse(view.show_lead_image())

        doc = PyQuery(view())
        self.assertFalse(doc('.leadimage'))

    def test_show_lead_image(self):
        image = StringIO(
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')

        self.entry.setLeadimage(image)

        view = self.entry.restrictedTraverse('@@blog_entry_view')
        self.assertFalse(view.show_lead_image())

        self.enable_lead_image()
        self.assertTrue(view.show_lead_image())

        doc = PyQuery(view())
        self.assertTrue(doc('.leadimage'))

