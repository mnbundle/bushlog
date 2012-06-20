from setuptools import setup, find_packages

setup(
    name = "bushlog",
    version = "0.1",
    url = 'http://www.bushlog.com',
    description = "Bushlog Web Application",
    author = 'Jonathan Bydendyk',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = [
        'setuptools',
        'django-bootstrap-toolkit',
    ],
)
