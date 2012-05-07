from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.tagging.browser.viewlets.taglist import TagListViewlet


class FtwBlogActionsBar(ViewletBase):
    """A Viewlet wich show the blog specific searchfield
    """

    render = ViewPageTemplateFile('ftw_blog_actionsbar.pt')


class HiddenTagList(TagListViewlet):
    """ Hide the Taglist from ftw.tagging """

    def update(self):
        pass

    def index(self):
        return ''
