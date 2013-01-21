import unittest2 as unittest
from ftw.blog.testing import FTW_BLOG_INTEGRATION_TESTING
from zope.interface import alsoProvides
from plone.app.discussion.interfaces import IDiscussionLayer
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone.app.discussion.interfaces import IDiscussionSettings
from ftw.blog.interfaces import IBlogLayer


class TestPatchedConversationView(unittest.TestCase):

    layer = FTW_BLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        # Allow discussion
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        settings.globally_enabled = True

        self.blog = self.portal.get(self.portal.invokeFactory('Blog', 'blog'))

    def test_enabled_original(self):

        # Provide IDiscussionLayer
        alsoProvides(
            self.portal.REQUEST, IDiscussionLayer)

        entry = self.blog.get(self.blog.invokeFactory('BlogEntry', 'entry'))
        view = entry.restrictedTraverse('@@conversation_view')

        self.assertFalse(view.enabled())

    def test_enabled_blog(self):

        # Provide IBlogLayer
        alsoProvides(
            self.portal.REQUEST, IBlogLayer)

        entry = self.blog.get(self.blog.invokeFactory('BlogEntry', 'entry'))
        view = entry.restrictedTraverse('@@conversation_view')

        self.assertTrue(view.enabled())
