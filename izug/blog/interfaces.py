from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from izug.simplelayout.interfaces import ISimpleLayoutContainer

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
    

