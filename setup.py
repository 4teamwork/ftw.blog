from setuptools import setup, find_packages

version = '0.1'

setup(name='izug.blog',
      version=version,
      description="iZug Quills configuration package.",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='izug quills blog',
      author='4teamwork.ch',
      author_email='info@4teamwork.ch',
      url='https://svn.4teamwork.ch/repos/zug/izug.blog',
      license='GPL',
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
