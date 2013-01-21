from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from zope.configuration import xmlconfig


class ZCMLLayer(ComponentRegistryLayer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.blog
        self.load_zcml_file('tests.zcml', ftw.blog.tests)
        self.load_zcml_file('configure.zcml', ftw.blog)


ZCML_LAYER = ZCMLLayer()


class FtwBlogLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import ftw.blog
        xmlconfig.file('configure.zcml', ftw.blog,
                       context=configurationContext)

        z2.installProduct(app, 'ftw.blog')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.blog:default')

        setRoles(portal, TEST_USER_ID, ['Contributor'])
        login(portal, TEST_USER_NAME)


FTW_BLOG_FIXTURE = FtwBlogLayer()
FTW_BLOG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_BLOG_FIXTURE,), name="FtwBlog:Integration")
FTW_BLOG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_BLOG_FIXTURE,), name='FtwBlog:Functional')
