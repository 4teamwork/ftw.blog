from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implements
from zope.interface import alsoProvides

from ftw.blog.interfaces import IBlogEntry
from ftw.blog import _


class IBlogEntrySchema(model.Schema):
    dexteritytextindexer.searchable('text')
    text = RichText(
        title=_('label_text', default=u"Text"),
        required=False
    )

    show_images = schema.Bool(
        title=_('label_show_images', default=u"Show images as gallery"),
        required=False,
    )

alsoProvides(IBlogEntrySchema, IFormFieldProvider)


class BlogEntry(Container):
    implements(IBlogEntry)
