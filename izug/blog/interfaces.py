from zope import schema
from zope.interface import Interface

from plone.portlets.interfaces import IPortletManager
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from izug.simplelayout.interfaces import ISimpleLayoutContainer
from zope.viewlet.interfaces import IViewletManager

from izug.blog import blogMessageFactory as _


class IBlogEntry(ISimpleLayoutContainer):
    """iZug Blog Entry"""

class IBlogCategory(Interface):
    """iZug Blog Category"""

class IBlog(Interface):
    """iZug Blog"""

class IArchivable(Interface):
    """Archiveable"""

class ICategorizable(Interface):
    """Categorizeable"""

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


