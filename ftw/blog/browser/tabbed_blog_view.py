from ftw.tabbedview.browser.tabbed import TabbedView
from ftw.table import helper
from ftw.tabbedview.browser.listing import CatalogListingView
from ftw.blog import _


class BlogsView(TabbedView):
    """Tabbed blog overview"""

    def get_tabs(self):
        return [{'id':'blogs', 'class':''},
                {'id':'blogentries', 'class':''}, ]


class Tab(CatalogListingView):
    """Search for the hole plone site"""

    def __init__(self, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.filter_path = None

    def update_config(self):
        super(Tab, self).update_config()
        self.filter_path = '/'.join(
            self.context.portal_url.getPortalObject().getPhysicalPath())


class BlogsTab(Tab):

    types = 'Blog'
    sort_on = 'sortable_title'
    show_selects = False
    show_menu = False

    columns = (
        {'column': 'Title',
         'column_title': _(u'column_title', default=u'Title'),
         'sort_index': 'sortable_title',
         'transform': helper.linked},
         {'column': 'Creator',
          'column_title': _(u'column_creator', default=u'Creator'),
          'sort_index': 'sortable_creator',
          'transform': helper.readable_author}, )


class BlogEntriesTab(Tab):

    types = 'BlogEntry'
    sort_on = 'created'
    sort_reverse = True
    show_selects = False
    show_menu = False

    columns = (
        {'column': 'created',
         'column_title': _(u'column_created', default=u'created'),
         'transform': helper.readable_date},
        {'column': 'Title',
         'column_title': _(u'column_title', default=u'Title'),
         'sort_index': 'sortable_title',
         'transform': helper.linked},
         {'column': 'Creator',
          'column_title': _(u'column_creator', default=u'Creator'),
          'sort_index': 'sortable_creator',
          'transform': helper.readable_author}, )
