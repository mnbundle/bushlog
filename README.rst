Bushlog (1.0.0)
===============
A fun, interactive and open-source way to record and share wildlife sightings.

`www.bushlog.com`_


.. contents::


Contributing
------------

Contributions will be greatly appreciated. To contribute, fork the project and submit pull requests.

Setup Development Environment::

    $ git clone git@github.com:<your_github_username>/bushlog.git
    $ cd bushlog
    $ virtualenv .
    $ . bin/activate

    # install the requirements
    (bushlog)$ pip install -r requirements.pip

    # edit bushlog/settings/base.py - if required
    (bushlog)$ vi bushlog/settings/base.py

    # running the tests
    (bushlog)$ ./manage.py test

    # running the server
    (bushlog)$ ./manage.py runserver dev.bushlog.com:9000


.. _www.bushlog.com: http://www.bushlog.com
