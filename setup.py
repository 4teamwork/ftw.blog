import os
from setuptools import setup, find_packages

version = open('ftw/blog/version.txt').read().strip()

maintainer = 'Mathias Leimgruber'

tests_require = [
    'collective.testcaselayer',
    ]

setup(name='ftw.blog',
      version=version,
      description="ftw Quills configuration package. (Maintainer: %s)" % maintainer,
      long_description=open("README.txt").read() + "\n" +
	                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='ftw blog',
      author='%s, 4teamwork.ch' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      url='http://psc.4teamwork.ch/4teamwork/kunden/ftw/ftw.blog/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
          # -*- Extra requirements: -*-
      ],
      extras_require={
        'tests_require': tests_require,
        },
      tests_require=tests_require,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
