from setuptools import setup, find_namespace_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='swachhdata',
    version='1.2.4',
    author='Kritik Seth',
    author_email='sethkritik@gmail.com',
    description='Data cleaning made easy with swachhdata',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kritikseth/swachhdata',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta'
    ],
    packages=find_namespace_packages(include=['swachhdata', 'swachhdata.*']),
    install_requires=[
        'regex>=2019.12.20',
        'pandas>=1.1.4',
        'tqdm>=4.41.1',
        'bs4>=0.0.1',
        'beautifulsoup4>=4.6.3',
        'html5lib>=1.0.1',
        'contractions>=0.0.25',
        'emoji>=0.6.0',
        'nltk>=3.2.5',
        'spacy>=2.2.4',
        'gensim>=3.6.0',
        'num2words>=0.5.10',
        'textblob>=0.15.3',
        'requests>=2.23.0',
        'opencv-python>=4.1.2.30',
        'tweepy>=3.6.0'
    ]
)