# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument

from ftw.blog import _
from zope import schema
from zope.interface import Interface


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
    """Widget for selecting categories.
    """


class IBlogView(Interface):
    """
    Marker Interface for BlogView
    """


class IBlogEntryView(Interface):
    """
    Marker Interface for BlogView
    """


class IBlogUtils(Interface):
    """
    provides Blog utilities
    """

    def getBlogRoot(context):
        """Returns the blog root of the current context. If the context is
        not within a blog, `None` is returned.
        """


class IBlogSettings(Interface):
    """Blog settings"""

    blog_entry_has_lead_image = schema.Bool(
        title=_(u"Show lead image in blog entries"),
        default=False)
