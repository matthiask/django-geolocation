#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='django-geolocation',
    version='1.0',
    description='django-geolocation',
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='https://github.com/matthiask/django-geolocation/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=[],
    ),
    install_requires=[
        'Django>=1.4.2',
        # Yes, form_designer can be used without FeinCMS.
    ],
    zip_safe=False,
)
