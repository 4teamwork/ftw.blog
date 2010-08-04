from Products.PloneTestCase import ptc
from collective.testcaselayer import common
from collective.testcaselayer import ptc as tcl_ptc


class Layer(tcl_ptc.BasePTCLayer):
    """Install ftw.blog """

    def afterSetUp(self):
        ptc.installPackage('ftw.blog')
        self.addProfile('ftw.blog:default')

layer = Layer([common.common_layer])
