Editing Django models in the front end
======================================

.. image:: https://readthedocs.org/projects/editing-django-models-in-the-frontend/badge/?version=latest
    :target: https://editing-django-models-in-the-frontend.readthedocs.io/en/latest/?badge=latest

See full documentation at:
https://editing-django-models-in-the-frontend.readthedocs.io

Purpose
-------

I try to take advantage of the powerful Django admin in all my web projects, at least in the beginning.

However, as the project evolves and the frontend improves, the usage of the admin tends to be more and more residual.

Adding editing capabilities to the frontend in a modern user interface requires the usage of modal forms, which, to be honest, have always puzzled me for some reason.

**This project is not a reusable Django package (not yet, at least)**, but rather a collection of techniques and examples used to cope with modal popups, form submission and validation via ajax, and best practices to organize the code in an effective way to minimize repetitions.

Any interest in having these techniques packaged as a reusable Django app ?
If so, please let me know by leaving a comment in the issue tracker.

.. figure:: ./docs/source/_static/images/main_screen.png

Installation
------------

Download the project::

    $ git clone https://github.com/morlandi/editing-django-models-in-the-frontend.git
    $ cd editing-django-models-in-the-frontend

Make a new virtualenv for the project, activate and update it::

    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt

build the database::

    $ cd sample_project
    $ python manage.py migrate

create a superuser to work with::

    $ python manage.py createsuperuser --username admin

then::

    $ python manage.py runserver

and visit the projects at http://127.0.0.1:8000/

Project requirements
--------------------

I happen to use:

- django v2.1.5
- jquery v3.3.1
- jquery-ui v1.12.1 (only required for draggable)
- django-bootstrap3 v11.0.0

but the techniques investigated should be usable in similar contexts.

A full explanation of what is going on under the hood is here:

https://editing-django-models-in-the-frontend.readthedocs.io

License
-------
Copyright &copy; 2018 Mario Orlandi.

MIT licensed.

