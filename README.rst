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

This project is not a reusable Django package, but rather a collection of techniques and examples used to cope with modal popups, form submission and validation via ajax, and best practices to organize the code in an effective way to minimize repetitions.

.. figure:: ./docs/source/_static/images/main_screen.png

Installation
------------

Make a new virtualenv for the project, and run::

    pip install -r requirements.txt

build the database::

    cd sample_project
    python manage.py migrate

create a superuser to work with::

    python manage.py createsuperuser --username admin

then::

    python manage.py runserver

and visit the projects at http://127.0.0.1:8000/

Project requirements
--------------------

I happen to use:

- django v2.1.1
- jquery v3.3.1
- jquery-ui v1.12.1 (only required for draggable)
- django-bootstrap3 v11.0.0

but the techniques investigated should be usable in similar contexts.


Documentation, installation and instructions are at
https://editing-django-models-in-the-frontend.readthedocs.io

License
-------
Copyright &copy; 2018 Mario Orlandi.

MIT licensed.

