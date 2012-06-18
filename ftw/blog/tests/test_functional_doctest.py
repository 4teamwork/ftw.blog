from ftw.blog.testing import FTW_BLOG_INTEGRATION_TESTING
from plone.testing import layered
import doctest
import unittest2 as unittest


OPTIONFLAGS = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS |
               doctest.REPORT_NDIFF)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
            layered(doctest.DocFileSuite('blog.txt',
                                         optionflags=OPTIONFLAGS),
                    layer=FTW_BLOG_INTEGRATION_TESTING),
            ])
    return suite
