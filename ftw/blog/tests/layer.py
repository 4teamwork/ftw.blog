from Products.PloneTestCase import ptc
from Testing import ZopeTestCase

import collective.testcaselayer.ptc

ptc.setupPloneSite()

# for FSS blablabla
import os
import Globals
from zope.component import getUtility

STORAGE_PATH = os.path.join(Globals.INSTANCE_HOME, 'var', 'fss_storage')
BACKUP_PATH = os.path.join(Globals.INSTANCE_HOME, 'var', 'fss_backup')

for base_path in (STORAGE_PATH, BACKUP_PATH):
    if not os.path.exists(base_path):
        os.mkdir(base_path)


class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):          
        import iw.fss
        self.addProfile('iw.fss:default')
        self.loadZCML('meta.zcml', package=iw.fss)

        
        ZopeTestCase.installPackage('ftw.blog')
        self.addProfile('ftw.blog:default')
        #self.addProduct('ftw.blog')
        
        

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])