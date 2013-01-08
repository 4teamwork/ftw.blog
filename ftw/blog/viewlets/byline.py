from plone.app.layout.viewlets import content
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DocumentBylineViewlet(content.DocumentBylineViewlet):

    index = ViewPageTemplateFile("blog_byline.pt")

    def show(self):
        return True

    def review_state(self):
        wftool = getToolByName(self.context, "portal_workflow")
        return wftool.getInfoFor(self.context, 'review_state')

    def creator(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(self.context.Creator())
        if member:
            return {
                'id': member.id,
                'name': member.getProperty('fullname') or member.id}
        return None
