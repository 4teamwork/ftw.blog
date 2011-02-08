from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import safe_hasattr
from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from ftw.blog.portlets import categories, archiv
from ftw.tagging.portlets import tags
from Products.CMFCore.utils import getToolByName


def objectAddedHandler(obj, event):
    """Handle IObjectAddedEvent
    """

    #adding a categories root object
    if not safe_hasattr(obj.aq_explicit, 'categories', False):
        _createObjectByType('BlogCategory', obj, 'categories')
        category = getattr(obj.aq_explicit, 'categories', False)
        if category:
            category.setTitle('Kategorien')
            category.reindexObject()

    category = getattr(obj.aq_explicit, 'categories', False)
    if not safe_hasattr(category.aq_explicit, 'allgemein', False):
        _createObjectByType('BlogCategory', category, 'allgemein')
        allgemein = getattr(category.aq_explicit, 'allgemein', False)
        if allgemein:
            allgemein.setTitle('Allgemein')
            allgemein.reindexObject()


def objectInitializedHandler(obj, event):
    #adding some portlets (archive/tags/categories)
    blog_manager = getUtility(
        IPortletManager,
        name=u'blog.portlets',
        context=obj)
    portlets = getMultiAdapter(
        (obj, blog_manager, ),
        IPortletAssignmentMapping,
        context=obj)

    category = 'blog-categories-portlet'
    if category not in portlets.keys():
        portlets[category] = categories.Assignment()
    a = 'blog-archive-portlet'
    if a not in portlets.keys():
        portlets[a] = archiv.Assignment()
    tagcloud = 'ftw.tagging.portlet.tagcloud'
    if tagcloud not in portlets.keys():
        portlets[tagcloud] = tags.Assignment()


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
