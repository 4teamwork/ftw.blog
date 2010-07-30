from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager
from zope.viewlet.interfaces import IViewletManager


class IBlogLayer(Interface):
    """ blog specific request layer interface
    """


class IBlogEntry(Interface):
    """Ftw BlogEntry"""


class IBlogCategory(Interface):
    """Ftw BlogCategory"""


class IBlog(Interface):
    """Ftw Blog"""


class ICategoryWidget(Interface):
    """
    """


class IBlogPortlets(IPortletManager):
    """Portlet manager for the blog
    """


class IBlogView(Interface):
    """
    Marker Interface for BlogView
    """


class IBlogEntryView(Interface):
    """
    Marker Interface for BlogView
    """


class IBlogBelowContent(IViewletManager):
    """
    """


class IBlogUtils(Interface):
    """
    provides Blog utilities
    """
