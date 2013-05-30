from ftw.blog.testing import FTW_BLOG_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from unittest2 import TestCase
from pyquery import PyQuery
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

        self.blog = self.portal.get(self.portal.invokeFactory('Blog', 'blog'))
        transaction.commit()

    def test_add_blog_entry(self):
        self.browser.open(
            "%s/createObject?type_name=BlogEntry" % self.blog.absolute_url())
        self.browser.getControl(name='title').value = 'Blog Entry'
        self.browser.getControl(name='form.button.save').click()

        self.assertEquals(len(self.blog.objectIds()), 1,
                          'Expect one blog entry')

        doc = PyQuery(self.browser.contents)
        self.assertEquals(doc('.documentFirstHeading').text(), 'Blog Entry',
                          'Wrong title found')
