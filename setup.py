from setuptools import setup, find_packages

setup(
    name="bluetrain",
    packages=[
            "bluetrain",
            "bluetrain.templatetags",
    ],
    package_data={
        "bluetrain": ["templates/*.html", "fixtures/*.json"],
    },
    include_package_data=True,
    version="0.9.8.1",
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
