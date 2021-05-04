from distutils.core import setup
from setuptools import find_packages

setup(
    name='retector',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'py-solc',
        'semantic_version',
        'graphviz',
        'py-etherscan-api'
    ],
    entry_points={
            'console_scripts': [
                'retector = retector.__main__:main'
            ]
    }
)
