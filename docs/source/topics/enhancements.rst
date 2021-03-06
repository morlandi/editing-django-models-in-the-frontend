Possible enhancements
=====================

The Django admin offers a rich environment for data editing; we might further
evolve our code to provide similar functionalities:

    Dynamic default values
        accept optional "initial" values from the url parameters in the "add new" view;
        useful for example to set a parent relation

    Fieldsets
        Check this for inspiration: https://schinckel.net/2013/06/14/django-fieldsets/

    Filtered lookup of related models
        As ModelAdmin does with **formfield_for_foreignkey** and **formfield_for_manytomany**

    Support for raw_id_fields
        Check https://github.com/lincolnloop/django-dynamic-raw-id/
        and https://www.abidibo.net/blog/2015/02/06/pretty-raw_id_fields-django-salmonella-and-django-grappelli/

    Support for inlines
        ...

    Support for autocompletion
        ...

Minor issues:

- Add a localized datepicker in the examples
- Add a ModelMultipleChoiceField (with multiSelect javascript widget) example in the sample project
- Accept and optional "next" parameter for redirection after successfull form submission (for standalone pages only)

