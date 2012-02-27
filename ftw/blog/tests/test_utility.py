from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ftw.blog.interfaces import IBlog
from ftw.blog.interfaces import IBlogUtils
from ftw.blog.testing import ZCML_LAYER
from ftw.blog.utility import BlogUtils
from ftw.testing import MockTestCase
from zope.component import getUtility
from zope.interface.verify import verifyClass


class TestUtility(MockTestCase):

    layer = ZCML_LAYER

    def test_component_registered(self):
        utils = getUtility(IBlogUtils, name='ftw.blog.utils')
        self.assertEqual(type(utils), BlogUtils)

    def test_component_implements_interface(self):
        self.assertTrue(IBlogUtils.implementedBy(BlogUtils))
        verifyClass(IBlogUtils, BlogUtils)

    def test_getBlogRoot_within_blog(self):
        blog = self.providing_stub([IBlog])
        obj = self.set_parent(
            self.stub(), self.set_parent(
                self.stub(), blog))

        self.replay()

        utils = getUtility(IBlogUtils, name='ftw.blog.utils')
        self.assertEqual(utils.getBlogRoot(obj), blog)

    def test_getBlogRoot_with_blog(self):
        blog = self.providing_stub([IBlog])

        self.replay()

        utils = getUtility(IBlogUtils, name='ftw.blog.utils')
        self.assertEqual(utils.getBlogRoot(blog), blog)

    def test_getBlogRoot_without_blog(self):
        site = self.providing_stub([IPloneSiteRoot])
        obj = self.set_parent(self.stub(), site)

        self.replay()

        utils = getUtility(IBlogUtils, name='ftw.blog.utils')
        self.assertEqual(utils.getBlogRoot(obj), None)
