from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.blog import _
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.portlets import base
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import PathSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implements


class IBlogEntryCollectionPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=_(u'label_title', default=u'Title'),
        required=True)

    show_image = schema.Bool(
        title=_(u'label_show_image', default=u'Show lead images'),
        default=True)

    path = schema.List(
        title=_(u"Blogs"),
        description=_(u"Decide where to collect BlogEntries"),
        value_type=schema.Choice(
            source=PathSourceBinder(
                navigation_tree_query={
                    'portal_type': 'Blog'}),
        ),
        required=False,
    )

    quantity = schema.Int(
        title=_(u'label_quantity', default=u'Quantity'),
        default=5)

    show_desc = schema.Bool(
        title=_(u'label_show_desc', default=u"Show Description"),
        default=True)


class Assignment(base.Assignment):
    implements(IBlogEntryCollectionPortlet)

    def __init__(self, portlet_title="BlogEntries", show_image=True, path=None,
                 quantity=5, show_desc=True):
        self.portlet_title = portlet_title
        self.show_image = show_image
        self.path = path
        self.quantity = quantity
        self.show_desc = show_desc

    @property
    def title(self):
        return _(u'label_portlet_title', default=u'BlogEntries collection')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('blogentry_collection_portlet.pt')

    def get_items(self):
        query = {'portal_type': 'BlogEntry',
                 'sort_on': 'created',
                 'sort_order': 'descending'}

        if self.data.path:
            query['path'] = self.data.path
        else:
            query['path'] = getNavigationRoot(self.context)

        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)


class AddForm(form.AddForm):
    implements(IBlogEntryCollectionPortlet)

    label = _(u'label_add_blogentry_collection_portlet',
              default=u'Add BlogEntry collection portlet')

    fields = field.Fields(IBlogEntryCollectionPortlet)

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
        self.status = None
        self._finishedAdd = None

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)

    def add(self, object_):
        ob = self.context.add(object_)
        self._finishedAdd = True
        return ob

    def updateWidgets(self):
        self.fields['path'].widgetFactory = MultiContentTreeFieldWidget
        super(AddForm, self).updateWidgets()

    def create(self, data):
        return Assignment(
            portlet_title=data.get('portlet_title', 'BlogEntries'),
            show_image=data.get('show_image', True),
            path=data.get('path', []),
            quantity=data.get('quantity', 5),
            show_desc=data.get('show_desc', True))


class EditForm(form.EditForm):
    implements(IBlogEntryCollectionPortlet)
    label = _(u'label_edit_blogentry_collection_portlet',
              default=u'Edit BlogEntry collection portlet')

    fields = field.Fields(IBlogEntryCollectionPortlet)

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.status = None
        self._finishedAdd = None

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)

    def updateWidgets(self):
        self.fields['path'].widgetFactory = MultiContentTreeFieldWidget
        super(EditForm, self).updateWidgets()
