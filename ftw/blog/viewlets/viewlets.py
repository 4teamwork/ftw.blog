from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.tagging.browser.viewlets.taglist import TagListViewlet

# TODO : Evtl. it can be solved with a better solution

# Use a Browserpage instead of the viewlet, 
# becauase we insert the serachbox with js
# For mor information have a look to entry.pt or blog.pt and plone.app.jquerytools.browser.overlayhelper.js

class FtwBlogActionsBar(ViewletBase):
  """ A Viewlet wich show the blog specific searchfield """
  render = ViewPageTemplateFile('ftw_blog_actionsbar.pt')

class HiddenTagList(TagListViewlet):
    """ Hide the Taglist from ftw.tagging """

    def update(self):
        pass
        
    def index(self):
        return ''

