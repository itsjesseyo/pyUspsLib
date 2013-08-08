from distutils.core import setup

setup(
    name='pyUspsLib',
    version='0.1.1',
    author='Jesse Gomez',
    author_email='jesse@luxnovalabs.com',
    packages=['pyuspslib'],
    url='http://pypi.python.org/pypi/pyUspsLib/',
    license='LICENSE',
    description='This package gives you access to all the usps apis',
    long_description=open('README.md').read(),
    install_requires=[
        "requests==1.2.3",
    ],
)