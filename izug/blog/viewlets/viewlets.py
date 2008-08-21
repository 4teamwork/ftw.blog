from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class izugBlogActionsBar(ViewletBase):
    render = ViewPageTemplateFile('izug_blog_actionsbar.pt')
