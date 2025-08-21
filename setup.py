from setuptools import setup, find_packages
setup(
    name='market-data-stream-analyzer',
    version='0.1.0',
    author = 'Harshit',
    description='A CLI tool to analyze and visualize market data from JSON streams.',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'mdsa=src.main:main',
        ],
    },
)