from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.discussion.interfaces import IConversation
from plone.batching import Batch
from zope.component import getMultiAdapter
from zope.interface import implements

from ftw.blog.interfaces import IBlogView, IBlogEntry
from ftw.tagging.behaviors.tagging import ITaggableSchema


class BlogView(BrowserView):
    """This view renders a single blog entry.
    """

    implements(IBlogView)

    def get_all_blog_entries(self):

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        query = {'object_provides': IBlogEntry.__identifier__,
                 'path': '/'.join(context.getPhysicalPath())}

        self.tagsfilter(query)

        brains = catalog(**query)

        return brains

    def tagsfilter(self, query):
        tag = self.request.form.get('tag')
        if tag:
            query['tags'] = tag

    def get_batch_results(self):
        return Batch.fromPagenumber(self.get_all_blog_entries(), pagesize=2,
                                    pagenumber=self.request.get('b_start', 0))

    def get_creator(self, item):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(item.Creator)
        return {
            'id': member.id,
            'name': member.getProperty('fullname') or member.id
        } if member else None

    def get_nb_comments(self, brain):
        obj = brain.getObject()
        conversation = IConversation(obj)
        return len([thread for thread in conversation.getThreads()])

    def get_tags(self, brain):
        obj = brain.getObject()
        tags = ITaggableSchema(obj).tags
        return tags

    def comments_enabled(self, brain):
        conversation = getMultiAdapter(
            objects=(brain.getObject(), self.request),
            name='conversation_view')
        return conversation.enabled()
