
from setuptools import setup, find_packages

setup(
    name='feedloggr',
    version='0.3',
    description='Collect news from your favorite RSS/Atom feeds and show them in your flask application.',
    long_description=open('README.md').read(),
    url='http://github.org/lmas/feedloggr',
    author='A. Svensson',
    author_email='lmasvensson at gmail dot com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask',
        'flask-script',
        'flask-peewee',
    ],
    # List of classifiers:  https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Private :: Do Not Upload'
    ],
)
