import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='service_core',
    version='0.1',
    include_package_data=True,
    license='MIT License',
    description='A common lib for nameko services.',
    long_description=README,
    author='Anderson Macedo',
    author_email='anderson.krs95@gmail.com',
    packages=find_packages(),
    install_requires=[
        'nameko>=2.8.5',
        'mixer>=6.0.0',
        'pytest>=3.5.0',
    ],
    extras_require={
        'test': [
            'testfixtures>=6.0.1'
        ],
    },
    entry_points={
        'pytest11': [
            'pytest_service_core=service_core.testing.pytest',
        ]
    },
    url='www.github.com/AndersonSKM/Buckets',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Nameko',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
