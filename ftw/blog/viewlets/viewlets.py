from ftw.tagging.browser.viewlets.taglist import TagListViewlet


class HiddenTagList(TagListViewlet):
    """ Hide the Taglist from ftw.tagging """

    def update(self):
        pass

    def index(self):
        return ''
