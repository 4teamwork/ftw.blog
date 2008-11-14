from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import safe_hasattr

def objectAddedHandler(object, event):
    """Handle IObjectAddedEvent
    """
    
    if not safe_hasattr(object, 'categories', False):
        _createObjectByType('Blog Category', object, 'categories')
        category = getattr(object, 'categories', False)
        if category:
            category.setTitle('Kategorien')
            category.reindexObject()
