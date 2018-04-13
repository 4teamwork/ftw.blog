import os
from setuptools import setup, find_packages

version = '1.8.1'

maintainer = 'Mathias Leimgruber'

tests_require = [
    'ftw.builder',
    'ftw.pdfgenerator',
    'ftw.testbrowser',
    'ftw.testing',
    'ftw.zipexport',
    'plone.app.testing',
    'plone.formwidget.contenttree',
    'pyquery',
    ]

setup(name='ftw.blog',
      version=version,
      description="A Blog for Plone",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      keywords='ftw blog',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.blog',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'ftw.colorbox',
        'ftw.tagging',
        'ftw.upgrade>=1.6.0',
        'ftw.pdfgenerator',
        'ftw.profilehook',
        'Plone',
        'plone.browserlayer',
        'plone.formwidget.contenttree',
        'setuptools',
        # -*- Extra requirements: -*-
        ],
      tests_require=tests_require,
      extras_require= {
          'tests': tests_require,
          'tabbeview': ['ftw.tabbedview'],
          'zip_export': ['ftw.zipexport']},

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
