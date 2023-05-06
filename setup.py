import os
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

import swachhdata

setuptools.setup(
    name='swachhdata',
    version=swachhdata.__version__,
    author=swachhdata.__author__,
    author_email='sethkritik@gmail.com',
    description='Data cleaning made easy with swachhdata',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=swachhdata.__url__,
    classifiers=[
        'Natural Language :: English',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Development Status :: 6 - Mature'
    ],
    packages=setuptools.find_namespace_packages(include=['swachhdata', 'swachhdata.*']),
    install_requires=[
        'regex>=2019.12.20',
        'pandas>=1.1.4',
        'tqdm>=4.41.1',
        'beautifulsoup4>=4.6.3',
        'html5lib>=1.0.1',
        'contractions>=0.0.25',
        'nltk>=3.6.5',
        'spacy>=2.2.4',
        'gensim>=3.6.0',
        'num2words>=0.5.10',
        'textblob>=0.15.3',
        'requests>=2.23.0',
        'opencv-python>=4.1.2.30',
        'tweepy>=3.6.0',
    ]
)