import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='core',
    version='0.1',
    include_package_data=True,
    license='MIT License',
    description='A core app with base classes.',
    long_description=README,
    author='Anderson Macedo',
    author_email='anderson.krs95@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Django>=2.0',
        'django-dirtyfields>=1.3.1',
        'django-filter>=2.0.0.dev1',
        'djangorestframework>=3.7.7',
        'djangorestframework-jwt>=1.11.0',
        'mixer>=6.0.0',
        'pytest>=3.1.3',
    ],
    extras_require={
        'test': ['testfixtures>=6.0.1'],
    },
    url='www.github.com/AndersonSKM/Buckets',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
