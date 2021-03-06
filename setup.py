from setuptools import setup

setup(name='planex',
      version='0.6.0',
      packages=['planex'],
      include_package_data = True,
      package_data={
	'planex':['Makefile.rules']
	},
      data_files=[('/usr/share/planex',['planex/Makefile.rules'])],
      entry_points={
          'console_scripts': [
              'planex-init = planex.init:main',
              'planex-configure = planex.configure:_main',
              'planex-build = planex.build:main',
              'planex-clone = planex.clone:main',
              'planex-cache = planex.cache:_main',
              'planex-downloader = planex.downloader:main',
              'planex-makedeb = planex.makedeb:main',
              'planex-depend = planex.depend:main'
          ]
      })
