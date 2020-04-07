import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'dropplets_api', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
            else:
                msg = 'Cannot find version in dropplets_api/__init__.py'
                raise RuntimeError(msg)


install_requires = ['aiohttp',
                    'cchardet',
                    'aiodns',
                    'asyncpg',
                    'passlib',
                    'trafaret-config',
                    'aioredis',
                    'aiohttp_session[aioredis]',
                    'aiohttp_security[session]',
                    'Unidecode'] # to remove diacritics with unidecode(string)]


setup(name='dropplets_api',
      version=read_version(),
      description='Core package for Dropplets project',
      platforms=['POSIX'],
      packages=find_packages(),
      package_data={
          '': ['static/*.*']
      },
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)
