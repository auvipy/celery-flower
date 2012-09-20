====================================================
 celerymon - Real-time monitoring of Celery workers
====================================================

:Version: 1.0.0

Installation
=============

You can install ``celerymon`` either via the Python Package Index (PyPI)
or from source.

To install using ``pip``,::

    $ pip install celerymon

To install using ``easy_install``,::

    $ easy_install celerymon

Downloading and installing from source
--------------------------------------

Download the latest version of ``celerymon`` from
http://pypi.python.org/pypi/celerymon/

You can install it by doing the following,::

    $ tar xvfz celerymon-0.0.0.tar.gz
    $ cd celerymon-0.0.0
    $ python setup.py build
    # python setup.py install # as root

Using the development version
------------------------------

You can clone the repository by doing the following::

    $ git clone git://github.com/celery/celerymon.git


Usage
=====

Running the monitor
-------------------

Start celery with the ``--events`` option on, so celery sends events for
celerymon to capture::

    $ python manage.py celeryd -E

Run the monitor server::

    $ python manage.py celerymon


However, in production you probably want to run the monitor in the
background, as a daemon:: 

    $ python manage.py celerymon --detach


For a complete listing of the command line arguments available, with a short
description, you can use the help command::

    $ python manage.py help celerymon


Now you can visit the webserver celerymon starts by going to:
http://localhost:8989


Mailing list
------------

For discussions about the usage, development, and future of celery,
please join the `celery-users`_ mailing list. 

.. _`celery-users`: http://groups.google.com/group/celery-users/

IRC
---

Come chat with us on IRC. The **#celery** channel is located at the `Freenode`_
network.

.. _`Freenode`: http://freenode.net


Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them
to our issue tracker at http://github.com/celery/celerymon/issues/

Contributing
============

Development of ``celerymon`` happens at Github:
http://github.com/celery/celerymon

You are highly encouraged to participate in the development
of ``celerymon``. If you don't like Github (for some reason) you're welcome
to send regular patches.

License
=======

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
