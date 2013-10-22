from ftw.blog.interfaces import IBlogSettings
from ftw.blog.testing import FTW_BLOG_INTEGRATION_TESTING
from plone.app.discussion.interfaces import IDiscussionLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from pyquery import PyQuery
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import getUtility
from zope.interface import alsoProvides


class TestLeadImage(TestCase):

    layer = FTW_BLOG_INTEGRATION_TESTING

    def setUp(self):
        super(TestLeadImage, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.blog = self.portal.get(self.portal.invokeFactory('Blog', 'blog'))
        self.entry = self.blog.get(
            self.blog.invokeFactory('BlogEntry', 'entry'))

        # Provide IDiscussionLayer for blog view
        alsoProvides(
            self.portal.REQUEST, IDiscussionLayer)

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

        view.request['ACTUAL_URL'] = self.entry.absolute_url()
        doc = PyQuery(view())
        self.assertFalse(doc('.leadimage'))

    def test_show_lead_image(self):
        image = StringIO(
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')

        view = self.entry.restrictedTraverse('@@blog_entry_view')
        view.request['ACTUAL_URL'] = self.entry.absolute_url()
        self.assertFalse(view.show_lead_image())

        blogview = self.blog.restrictedTraverse('@@blog_view')
        blogview.request['ACTUAL_URL'] = self.blog.absolute_url()
        doc = PyQuery(blogview())
        self.assertFalse(doc('.EntryLeadImage img'),
                         'There should be no image')

        self.entry.setLeadimage(image)

        self.enable_lead_image()
        self.assertTrue(view.show_lead_image())

        doc = PyQuery(view())
        self.assertTrue(doc('.leadimage'))

        doc = PyQuery(blogview())
        self.assertTrue(doc('.EntryLeadImage img'), 'There should be an image')
