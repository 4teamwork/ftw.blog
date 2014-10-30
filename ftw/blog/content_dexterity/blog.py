from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements

from ftw.blog.interfaces import IBlog


class IBlogSchema(model.Schema):
    pass


class Blog(Container):
    implements(IBlog)

    # TODO: Prevent setting the default site.
