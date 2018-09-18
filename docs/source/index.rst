.. Editing Django models in the front end documentation master file, created by
   sphinx-quickstart on Fri Sep 14 10:56:34 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Editing Django models in the front end
======================================

I try to take advantage of the powerful Django admin in all my web projects, at least in the beginning.

However, as the project evolves and the frontend improves, the usage of the admin tends to be more and more residual.

Adding editing capabilities to the frontend in a modern user interface requires the usage of modal forms, which, to be honest, have always puzzled me for some reason.

This project is not a reusable Django package, but rather a collection of techniques and examples used to cope with modal popups, form submission and validation via ajax, and best practices to organize the code in an effective way to minimize repetitions.

.. figure:: /_static/images/main_screen.png

.. _topics:

Topics
------

.. toctree::
   :maxdepth: 2
   :caption: Contents:


   topics/basic_modals
   topics/diango_basic_modals
   topics/simple_content
   topics/form_validation
   topics/edit_a_django_model
   topics/edit_a_django_model_2
   topics/edit_any_django_model
   topics/enhancements
   topics/references
   topics/contributing

Sample code
-----------

A sample Django project which uses all techniques discussed here is available on Github:

https://github.com/morlandi/editing-django-models-in-the-frontend

Search docs
-----------

* :ref:`search`
