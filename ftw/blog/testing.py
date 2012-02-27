from plone.testing import Layer
from plone.testing import zca
from zope.configuration import xmlconfig


class ZCMLLayer(Layer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES,)

    def testSetUp(self):
        self['configurationContext'] = zca.stackConfigurationContext(
            self.get('configurationContext'))

        import ftw.blog
        xmlconfig.file('tests.zcml', ftw.blog.tests,
                       context=self['configurationContext'])
        xmlconfig.file('configure.zcml', ftw.blog,
                       context=self['configurationContext'])

    def testTearDown(self):
        del self['configurationContext']


ZCML_LAYER = ZCMLLayer()
