# from distutils.core import setup
from setuptools import setup
import os

from jollacn_bot_py import __version__

setup(
    name="jollacn_bot_py",
    packages=["jollacn_bot_py"],
    package_data={
        '': [
            'README.md',
            'LICENSE',
        ],
        'jollacn_bot_py': [
        ],
    },
    install_requires=[
        'docpie',
        'colorlog',
        'bs4',
        'requests[socks]',
        'html5lib',
        'html2text',
        'pika',
    ],
    version=__version__,
    cmdclass={
        'jollacn_bot_py': 'jollacn_bot_py.main:main',
    },
    author="TylerTemp",
    author_email="tylertempdev@gmail.com",
    # url="http://docpie.comes.today/",
    # download_url="https://github.com/TylerTemp/docpie/tarball/%s/" % __version__,
    license='MIT',
    description=("jolla cn bot"),
    keywords='jolla',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    platforms='any',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
