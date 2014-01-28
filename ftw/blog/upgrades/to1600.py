from ftw.upgrade import UpgradeStep


class NewPortlet(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-plone.formwidget.contenttree:default')

        self.setup_install_profile(
            'profile-ftw.blog.upgrades:1600')
