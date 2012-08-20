from distutils.core import setup

setup(
    name='bluetrain',
    packages=[
            'bluetrain',
            'bluetrain.fixtures',
            'bluetrain.templates',
            'bluetrain.templatetags',
    ],
    version='0.9.6.3',
    description='Django CMS',
    long_description=open('README.txt').read(),
    author='Tom Clancy',
    author_email='tclancy@gmail.com',
    url='https://bitbucket.org/tclancy/tkc_apps',
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
