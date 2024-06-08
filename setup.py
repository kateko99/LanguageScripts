import os
from setuptools import find_packages, setup

setup(
    name = "language_project",
    version = "1.0.0",
    author = "Katarzyna Kowalczyk",
    author_email = "kakowalczyk07@gmail.com",
    description = ("Some python scripts to manipulate text"),
    package_dir={"": "zadania_stazowe"},
    packages=find_packages(where="zadania_stazowe"),
    license = "BSD",
    keywords = "language script search",
    url = "https://github.com/kateko99/LanguageScripts",
    long_description = read('README'),
    classifiers=[
        "Topic :: Language scripts",
        "License :: OSI Approved :: BSD License",
    ],
)
