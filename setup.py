#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

version = get_version('ib_gamification_backend', '__init__.py')

if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

required_list = []
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()
    for each_required in required:
        if each_required.find("git+ssh") == -1:
            required_list.append(each_required)

setup(
    name='ib_gas',
    version=version,
    description="""Automate API generation from swagger""",
    long_description=readme + '\n\n' + history,
    author='iB Hubs',
    author_email='devops@ibtspl.com',
    url='https://bitbucket.org/rahulsccl/ib_gamification_backend-django',
    packages=[
        'ib_club',
        'ib_content_portal',
        'ib_digital_ads',
        'ib_game_env',
        'ib_game_object',
        'ib_gamification',
        'ib_gamification_backend',
        'ib_gamification_common',
        'ib_gamification_validation',
        'ib_match',
        'ib_mini_games',
        'ib_resource',
        'ib_score_board',
        'ib_shop',
        'ib_sponsorship',
        'ib_team',
        'ib_tournament',
        'ib_treasure',
        'ib_challenge',
        'ib_power_ups',
        'ib_consistency_reward',
        'ib_alarms',
        'ib_bookings',
        'ib_badges',
        'ib_bet',
        'ib_mini_games_public',
    ],
    include_package_data=True,
    install_requires=required_list,
    zip_safe=False,
    keywords='ib_gas',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

    ],
)
