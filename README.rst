Overview
========

``ftw.blog`` provides a blog implementation for Plone featuring tags and
categories.

A user can add a new blog entry and tag it using tags and categories.
Available categories are defined by the creator of the blog, whilst
tags can be added freely by the author of a blog entry.

Blog entries are listed in chronological order, in a tag cloud, by
categories, and in a monthly archive. Entries can be searched by using the
search function of the blog.

Enable commenting by activating the ``global_allowed`` setting in the ``@@discussion-settings`` view.

You can enable a lead image for BlogEntries (Configuration registry).
It's disabled by default. If enabled you are able to add an image to a BlogEntry.
It will be shown on the BlogEntry itself and on the Blog overview

BlogEntry collection portlet. This portlet lists blog entries sorted by
creation date. You can show blog entries of multiple blog instances. It's also
possible to show the leadimage and the description of a blog entry.

Install
=======

- Add ``ftw.blog`` to your buildout configuration

::

    [instance]
    eggs =
        ftw.blog

- Run buildout

- Install ``ftw.blog`` in portal_setup


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
