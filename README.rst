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

Optionally, blog entries can be commented by users using Plone's commenting
functionality.


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
