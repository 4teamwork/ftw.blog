from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.comments import CommentsViewlet


class FtwBlogActionsBar(ViewletBase):

    render = ViewPageTemplateFile('ftw_blog_actionsbar.pt')


class CommentsViewlet(CommentsViewlet):
    render = ViewPageTemplateFile('ftw_comments.pt')
