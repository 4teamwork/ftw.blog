from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.globals.interfaces import IViewView 
from zope.interface import implements, alsoProvides

class izugBlogActionsBar(ViewletBase):
    render = ViewPageTemplateFile('izug_blog_actionsbar.pt')

    def update(self):
        context = aq_inner(self.context)
        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')

        self.object_actions = context_state.actions().get('blog_actions', [])

        plone_utils = getToolByName(context, 'plone_utils')

        self.portal_actionicons = getToolByName(context, 'portal_actionicons')
        
        # The drop-down menus are pulled in via a simple content provider
        # from plone.app.contentmenu. This behaves differently depending on
        # whether the view is marked with IViewView. If our parent view 
        # provides that marker, we should do it here as well.
        if IViewView.providedBy(self.__parent__):
            alsoProvides(self, IViewView)
