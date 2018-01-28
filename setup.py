from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='sitewalker',
      version=version,
      description="Traverse site and represent it as a graph",
      long_description="""\
One script, given a URL, does a website crawl with depth up to N,
and writes some data to a JSON file. Other scripts investigate graph based on the saved
data.
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Web crawler, scraper, graph, sitemap',
      author='data.Sergey Krushinsky',
      author_email='krushinsky@gmail.com',
      url='http://crawlers.info/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
          setup_requires=['nose>=1.0'],
          install_requires=[
            'requests',
            'bs4',
            'lxml',
          ],
          tests_require=['nose>=1.0'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
