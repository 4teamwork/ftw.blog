from ftw.upgrade import UpgradeStep


class UpgradeBlogEntryFTI(UpgradeStep):

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.blog.upgrades:1201')
