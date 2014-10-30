Overview
========

``ftw.blog`` provides a very basic blog system for Plone
featuring tags, categories and optional image galleries per blog entry.

A user can add a new blog entry (title and text) and assign tags and (nested)
categories. Available categories are defined by the creator of the blog,
whilst tags can be added freely by the author of a blog entry. Files and
images can be added to a blog entry.

Blog entries are listed in chronological order, in a tag cloud, by
categories, and in a monthly archive. Entries can be searched by using the
search function of the blog.

If the gallery option has been enabled for a blog entry, thumbnails of
the entry's images are displayed below the text of the entry. An image slide
show is started by clicking on any of the thumbnails.

You can allow or disallow commenting per blog entry. Commenting needs
to be enabled globally for this to work. You can enable commenting in the
discussion settings of the Plone site configuration.

A lead image can be uploaded and added to a blog entry. This feature is
disabled by default and can be enabled in the configuration registry of
the Plone site. If enabled the lead image is displayed on the blog entry
itself and on the listing of all blog entries. Please note that the lead
image will only be displayed on the blog entry if the gallery is enabled
for the blog entry, though this will change in a future release)

Besides the tag cloud portlet, monthly archive portlet and categories portlet,
a *blog entry collection* portlet is available. This portlet lists blog
entries from multiple blogs, sorted by creation date. It's also possible to
display the lead image or the description of the blog entries rendered by the
portlet.

Install
=======

- Add ``ftw.blog`` to your buildout configuration

::

    [instance]
    eggs =
        ftw.blog

- Run buildout

- Install ``ftw.blog`` in portal_setup

Uninstall
=========

This package provides an uninstall Generic Setup profile, however, it will
not uninstall the package dependencies.
Make sure to uninstall the dependencies if you no longer use them.

Links
=====

- Package repository: https://github.com/4teamwork/ftw.blog
- Issue tracker: https://github.com/4teamwork/ftw.blog/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.blog
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.blog

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.blog`` is licensed under GNU General Public License, version 2.

.. image:: https://cruel-carlota.pagodabox.com/8b048ecd61dba82375e5662b30e6f0d6
   :alt: githalytics.com
   :target: http://githalytics.com/4teamwork/ftw.blog
