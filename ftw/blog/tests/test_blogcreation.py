# base imports
import unittest
import os

# Tests
from Products.PloneTestCase.ptc import PloneTestCase 

# Layer
from layer import Layer

class TestBlog(PloneTestCase): 
    
    layer = Layer
    
    def afterSetUp(self):
        #make blog generally available 
        self.loginAsPortalOwner()
        blog_type = self.portal.portal_types.Blog
        blog_type.manage_changeProperties(global_allow=True)
        
        # add some content.

        # dummy object to test the aquisition 
        testdummy = self.portal.invokeFactory('Folder', 'allgemein')
        
        #our blogs
        testblog1id = self.portal.invokeFactory('Blog', 'test-blog1')
        self.testblog1 = getattr(self.portal, 'test-blog1', None)
        testfolderid = self.portal.invokeFactory('Folder', 'folder1')
        self.testfolder = self.portal.folder1
        testblog2id = self.testfolder.invokeFactory('Blog', 'test-blog2')
        self.testblog2 = getattr(self.testfolder, 'test-blog2', None)


    def test_categories1(self):
        # check if events work correctly
        # there should be a categories category and a sucategory "allgemein"
        self.assertEquals(hasattr(self.testblog1.aq_explicit, 'categories'), True)
        categories = self.testblog1.aq_explicit.categories
        self.assertEquals(hasattr(categories.aq_explicit, 'allgemein'), True)
        

    def test_categories2(self):
        self.assertEquals(hasattr(self.testblog2.aq_explicit, 'categories'), True)
        categories = self.testblog2.aq_explicit.categories
        self.assertEquals(hasattr(categories.aq_explicit, 'allgemein'), True)












def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)