from ftw.blog.interfaces import IBlogSettings
from ftw.blog.testing import FTW_BLOG_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from pyquery import PyQuery
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

    def test_blog_entry_has_no_lead_image_by_default(self):

        field = self.entry.Schema()['leadimage']
        self.assertFalse(
            field.widget.testCondition(None, self.portal, self.entry))

    def test_blog_entry_has_lead_image(self):
        registry = getUtility(IRegistry)
        registry.forInterface(IBlogSettings).blog_entry_has_lead_image = True

        field = self.entry.Schema()['leadimage']
        self.assertTrue(
            field.widget.testCondition(None, self.portal, self.entry))
