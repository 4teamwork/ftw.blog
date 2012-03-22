from ftw.testing.layer import ComponentRegistryLayer


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
