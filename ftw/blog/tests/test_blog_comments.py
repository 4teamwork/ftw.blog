from ftw.blog.interfaces import IBlogLayer
from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope.interface import alsoProvides
import transaction


class TestBlogComments(TestCase):

    layer = FTW_BLOG_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.blog = self.portal[self.portal.invokeFactory('Blog', 'b1')]
        self.entry1 = self.blog[self.blog.invokeFactory('BlogEntry', 'e1')]
        self.entry2 = self.blog[self.blog.invokeFactory('BlogEntry', 'e2')]

        transaction.commit()

        self.set_allowAnonymousViewAbout_property(True)

        # Provide IBlogLayer
        alsoProvides(
            self.portal.REQUEST, IBlogLayer)

    def set_allowAnonymousViewAbout_property(self, value):
        site_props = getToolByName(
            self.portal, 'portal_properties').site_properties
        site_props._updateProperty('allowAnonymousViewAbout', value)
        transaction.commit()

    def is_author_visible(self, obj):
        self.browser.open(obj.absolute_url())
        return '<span class="documentAuthor">' in self.browser.contents

    def count_comments_tags(self, obj):
        self.browser.open(obj.absolute_url())
        return self.browser.contents.count('<div class="comments">')


class TestBlogCommentsAnonymous(TestBlogComments):

    def test_show_author_when_allowAnonymousViewAbout_on_blog(self):
        self.assertTrue(self.is_author_visible(self.blog),
                        '''Anonymous user should see author if
                        allowAnonymousViewAbout is True.''')

    def test_show_author_when_allowAnonymousViewAbout_on_blogentry(self):
        self.assertTrue(self.is_author_visible(self.entry1),
                        '''Anonymous user should see author if
                        allowAnonymousViewAbout is True.''')

    def test_dont_show_author_when_not_allowAnonymousViewAbout_on_blog(self):
        self.set_allowAnonymousViewAbout_property(False)
        self.assertFalse(self.is_author_visible(self.blog),
                        '''Anonymous user should not see author if
                        allowAnonymousViewAbout is False.''')

    def test_dont_show_author_when_not_allowAnonymousViewAbout_on_blogentry(self):
        self.set_allowAnonymousViewAbout_property(False)
        self.assertFalse(self.is_author_visible(self.entry1),
                        '''Anonymous user should not see author if
                        allowAnonymousViewAbout is False.''')

    def test_dont_show_comments_on_blog_overview_when_discussion_is_disabled(self):
        self.assertEquals(self.count_comments_tags(self.blog), 0,
                         '''There must be 0 comments tag because discussion is
                         disabled''')

    def test_show_comments_on_blog_overview_when_discussion_is_allowed(self):
        registry = getToolByName(self.portal, 'portal_registry')
        registry[
            'plone.app.discussion.interfaces.IDiscussionSettings.globally_enabled'] = True

        transaction.commit()

        self.assertEquals(self.count_comments_tags(self.blog), 2,
                         '''There must be 2 comments tag because discussion is
                         enabled''')


class TestBlogCommentsLoggedIn(TestBlogComments):

    def setUp(self):
        super(TestBlogCommentsLoggedIn, self).setUp()

        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_show_author_when_allowAnonymousViewAbout_on_blog(self):
        self.assertTrue(self.is_author_visible(self.blog),
                        '''Logged in user should see author if
                        allowAnonymousViewAbout is True.''')

    def test_show_author_when_allowAnonymousViewAbout_on_blogentry(self):
        self.assertTrue(self.is_author_visible(self.entry1),
                        '''Logged in user should see author if
                        allowAnonymousViewAbout is True.''')

    def test_show_author_when_not_allowAnonymousViewAbout_on_blog(self):
        self.set_allowAnonymousViewAbout_property(False)
        self.assertTrue(self.is_author_visible(self.blog),
                        '''Logged in user should see author
                        if allowAnonymousViewAbout is False.''')

    def test_show_author_when_not_allowAnonymousViewAbout_on_blogentry(self):
        self.set_allowAnonymousViewAbout_property(False)
        self.assertTrue(self.is_author_visible(self.entry1),
                        '''Logged in user should see author if
                        allowAnonymousViewAbout is False.''')
