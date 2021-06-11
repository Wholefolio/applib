from setuptools import setup

setup(name='applib',
      version='1.3.3',
      description='App library - common toolbox library for applications',
      url='http://gitlab.com/wholefolio/applib',
      author='Atanas K',
      author_email='support@wholefolio.io',
      license='MIT',
      packages=['applib'],
      install_requires=[
          'requests>2.21.0',
          'simplejson==3.17.2',
          'django>=2.2'
      ],
      zip_safe=False)
