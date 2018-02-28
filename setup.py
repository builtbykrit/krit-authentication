import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='krit-authentication',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple Django authentication app',
    long_description=README,
    url='https://www.builtbykrit.com',
    author='Kevin Hoffman',
    author_email='kevin@builtbykrit.com',
    install_requires=[
        'Django>=1.11.4',
        'django-appconf>=1.0.2',
        'django-rest-auth>=0.9.1',
        'djangorestframework>=3.6.4',
        'djangorestframework-jsonapi>=2.2.0',
        'python-http-client>=3.0.0',
        'urllib3>=1.22'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)