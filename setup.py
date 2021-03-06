from setuptools import setup, find_packages
from setuptools.command import sdist

del sdist.finders[:]

setup(

    # project description
    name='bushlog',
    version='1.0.0',
    description='Bushlog Web App',
    long_description="%s\n\n%s" % (open('README.rst', 'r').read(), open('AUTHORS.rst', 'r').read()),
    author='Jonathan Bydendyk',
    author_email='jpbydendyk@gmail.com',
    url='http://www.bushlog.com',

    # packaging
    packages=find_packages(),
    include_package_data=True,

    # dependancies
    dependency_links=[],
    install_requires=[
        'Django==1.5.4',
        'Markdown==2.3',
        'PIL==1.1.7',
        'South==0.7.6',
        'argparse==1.2.1',
        'django-appconf==0.6',
        'django-bootstrap-toolkit==2.8.0',
        'django-compressor==1.3',
        'django-filter==0.6a1',
        'django-suit==0.2.5',
        'django-social-auth==0.7.22',
        'djangorestframework==2.2.4',
        'flickrapi==1.4.2',
        'futures==2.1.3',
        'gunicorn==0.17.2',
        'httplib2==0.8',
        'oauth2==1.5.211',
        'python-dateutil==2.1',
        'python-instagram==0.8.0',
        'python-memcached==1.31',
        'python-openid==2.2.5',
        'python-twitter==1.0',
        'selenium==2.31.0',
        'simplejson==3.3.0',
        'six==1.3.0',
        'versiontools==1.9.1',
        'wsgiref==0.1.2',
        'beautifulsoup4==4.3.2'
    ],
    scripts=[
        'bushlog/bushlog.sh'
    ]
)
