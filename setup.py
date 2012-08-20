from setuptools import setup, find_packages

setup(
    name="bluetrain",
    packages=find_packages(),
    package_data={
        "bluetrain": ["templates/*.html", "fixtures/*.json"],
    },
    version="0.9.7.3",
    description="Django CMS",
    long_description=open("README.txt").read(),
    author="Tom Clancy",
    author_email="tclancy@gmail.com",
    url="https://github.com/tclancy/bluetrain",
    license="LGPL",
    classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Framework :: Django"
    ],
)
