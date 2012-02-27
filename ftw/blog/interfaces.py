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


class IBlogUtils(Interface):
    """
    provides Blog utilities
    """

    def getBlogRoot(context):
        """Returns the blog root of the current context. If the context is
        not within a blog, `None` is returned.
        """
