from setuptools import setup, find_packages

setup(
    name="zenscan",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-nmap",
        "wapiti3",
        "flask"
    ],
    entry_points={
        "console_scripts": [
            "zenscan = main:main"
        ]
    }
)
