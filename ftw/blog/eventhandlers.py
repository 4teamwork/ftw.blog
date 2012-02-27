from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import safe_hasattr
from ftw.blog import _


def objectAddedHandler(obj, event):
    """Handle IObjectAddedEvent
    """

    #adding a categories root object
    if not safe_hasattr(obj.aq_explicit, 'categories', False):
        _createObjectByType('BlogCategory', obj, 'categories')
        category = getattr(obj.aq_explicit, 'categories', False)
        if category:
            category.setTitle(obj.translate(_('Categories')))
            category.reindexObject()


def set_description(obj, event):
    """Get the first 200 Chars from text and set them as descrption
    Use portal_transforms to create plain-text
    """

    portal_transforms = getToolByName(obj, 'portal_transforms')
    ploneview = obj.restrictedTraverse('@@plone')
    text = obj.getField('text').get(obj)
    datastream = portal_transforms.convertTo(
        'text/plain',
        text,
        mimetype='text/html')
    plain_text = datastream.getData()
    # truncate
    length = 200
    truncated = ploneview.cropText(plain_text, length)
    obj.getField('description').set(obj, truncated)
    obj.reindexObject()
