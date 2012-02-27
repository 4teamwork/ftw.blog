from ftw.blog.interfaces import IBlog
from ftw.blog.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from mocker import ANY
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class TestBlogSettings(MockTestCase):

    layer = ZCML_LAYER

    def test_component_registered(self):
        blog = self.providing_stub([IBlog])
        request = self.providing_stub([IDefaultBrowserLayer])

        self.replay()
        # fails with ComponentLookupError when component not found:
        getMultiAdapter((blog, request), name='blog-settings')

    def test_getBlog(self):
        blog = self.providing_stub([IBlog])
        obj = self.set_parent(self.stub(), blog)
        request = self.providing_stub([IDefaultBrowserLayer])

        self.replay()
        view = getMultiAdapter((obj, request), name='blog-settings')
        self.assertEqual(view.getBlog(obj), blog)

    def test_objectActions(self):
        context_state = self.stub()
        self.mock_adapter(context_state, Interface,
                          (Interface, Interface), 'plone_context_state')
        self.expect(context_state(ANY, ANY)).result(context_state)
        self.expect(context_state.actions()).result(
            {'object_blog_settings_actions': ['manage_blog_portlets']})

        blog = self.providing_stub([IBlog])
        request = self.providing_stub([IDefaultBrowserLayer])

        self.replay()
        view = getMultiAdapter((blog, request), name='blog-settings')
        self.assertEqual(view.objectActions(), ['manage_blog_portlets'])

    def test_managePortletUrl(self):
        blog = self.providing_stub([IBlog])
        obj = self.set_parent(self.stub(), blog)
        request = self.providing_stub([IDefaultBrowserLayer])

        self.expect(blog.absolute_url()).result('http://nohost/plone/blog')

        self.replay()
        view = getMultiAdapter((obj, request), name='blog-settings')
        self.assertEqual(view.managePortletUrl(),
                         'http://nohost/plone/blog/@@manage-blog-portlets')

    def test_editBlog(self):
        blog = self.providing_stub([IBlog])
        obj = self.set_parent(self.stub(), blog)
        request = self.providing_stub([IDefaultBrowserLayer])

        self.expect(blog.absolute_url()).result('http://nohost/plone/blog')

        self.replay()
        view = getMultiAdapter((obj, request), name='blog-settings')
        self.assertEqual(view.editBlog(), 'http://nohost/plone/blog/edit')
