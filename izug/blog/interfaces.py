from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from izug.simplelayout.interfaces import ISimpleLayoutContainer
from plone.portlets.interfaces import IPortletManager

from izug.blog import blogMessageFactory as _

# -*- extra stuff goes here -*-

class IBlogEntry(ISimpleLayoutContainer):
    """iZug Blog Entry"""

class IBlogCategory(Interface):
    """iZug Blog Category"""

class IBlog(Interface):
    """iZug Blog"""

class ICategoryWidget(Interface):
    """
    """
    
class IBlogView(Interface):
    """
    Marker Interface for BlogView
    """

class IBlogEntryView(Interface):
    """
    Marker Interface for BlogView
    """
    
class IBlogPortlets(IPortletManager):
    """
    """


