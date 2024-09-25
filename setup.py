# setup.py

from setuptools import find_packages, setup

setup(
    name='auto_ip_alloc',
    version='0.1',
    description='Automatically allocate IP addresses from prefixes via REST API',
    url='https://github.com/andersalavik/auto_ip_alloc',
    author='Anders Alavik',
    author_email='anders.alavik@infracom.se',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
