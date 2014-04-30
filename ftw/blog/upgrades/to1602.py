from ftw.upgrade import UpgradeStep
from Products.CMFCore.utils import getToolByName


class RemoveImportSteps(UpgradeStep):

    def __call__(self):
        tool = getToolByName(self.portal, 'portal_setup')
        tool.manage_deleteImportSteps(['ftw.blog.catalog'])
