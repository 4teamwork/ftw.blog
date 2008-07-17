from StringIO import StringIO

# Zope imports
from zope.component import getUtility

# Plone imports
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.storage import PortletAssignmentMapping

# Quills imports
from quills.core.interfaces import IWeblog
from quills.core.interfaces import IWeblogEnhanced
from quills.app.portlets.context import INTERFACE_CATEGORY

from izug.blog.portlets import category_portlet

DEFAULT_LEFT_PORTLETS = (
    ('category_portlet', category_portlet.Assignment, {}),
    )

def weblogPortletSetup(context):
    portal = context.getSite()
    ifaces = [IWeblog, IWeblogEnhanced]
    out = StringIO()
    left_column  = getUtility(IPortletManager, name="plone.leftcolumn")
    try:
        left_category = left_column[INTERFACE_CATEGORY]
    except KeyError:
        left_column[INTERFACE_CATEGORY] = PortletAssignmentMapping()
        left_category = left_column[INTERFACE_CATEGORY]
    ifid = IWeblog.__identifier__
    left_portlets = left_category.get(ifid, None)
    # It may be that it hasn't been created yet, so just to be safe:
    if left_portlets is None:
        left_category[ifid] = PortletAssignmentMapping()
        left_portlets = left_category[ifid]
    for name, assignment, kwargs in DEFAULT_LEFT_PORTLETS:
        if not left_portlets.has_key(name):
            left_portlets[name] = assignment(**kwargs)
            # move to top
        keys = list(left_portlets.keys())
        keys.remove(name)
        keys.insert(0, name)
        left_portlets.updateOrder(keys)

