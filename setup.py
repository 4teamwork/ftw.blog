import os
from setuptools import setup, find_packages

version = '0.2'
maintainer = 'Mathias Leimgruber'

setup(name='izug.blog',
      version=version,
      description="iZug Quills configuration package. (Maintainer: %s)" % maintainer,
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
      keywords='izug quills blog',
      author='%s, 4teamwork.ch' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      url='http://psc.4teamwork.ch/4teamwork/kunden/izug/izug.blog/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['izug'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
