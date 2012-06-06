from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='smsd3',
      version=version,
      description="smsd3",
      long_description="""\
smsd3""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='sms',
      author='xbfool',
      author_email='xbfool@gmail.com',
      url='xbfool.org',
      license='private',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
