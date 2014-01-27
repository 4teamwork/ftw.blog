from ftw.blog.tests import builders
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
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

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import z3c.autoinclude
        xmlconfig.file('meta.zcml', z3c.autoinclude,
                       context=configurationContext)
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <includePlugins package="plone" />'
            '</configure>',
            context=configurationContext)

        import ftw.blog
        xmlconfig.file('configure.zcml', ftw.blog,
                       context=configurationContext)

        z2.installProduct(app, 'ftw.blog')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.blog:default')

        wftool = getToolByName(portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['Blog', 'BlogEntry'],
                                      'one_state_workflow')

        setRoles(portal, TEST_USER_ID, ['Contributor'])
        login(portal, TEST_USER_NAME)


FTW_BLOG_FIXTURE = FtwBlogLayer()
FTW_BLOG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_BLOG_FIXTURE,), name="FtwBlog:Integration")
FTW_BLOG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_BLOG_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name='FtwBlog:Functional')
