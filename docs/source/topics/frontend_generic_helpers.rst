Front-end generic helpers to work with any Model
================================================

Abbiamo realizzato una generic_edit_view() che provvede a gestire l'editing
di un oggetto arbitrario.

Tuttavia, l'introduzione nel front-end di nuovo Model ci costringe a scrivere
alcune istruzioni piuttosto ripetitive:

- una ModelForm specifica
- due url per invocare generic_edit_view() nei due casi "add" e "change"
  selezionando un valore opportuno per il parametro "model_form_class"
- i templates in cui inserire i link richiesti, che saranno presumibilmente
  analoghi a quelli gia' realizzati per altri Models.

Se il front-end prevede un numero limitato di Models, puo' essere ragionevole
accettare queste ripetizioni;
in caso contrario puo' valere la pena ricorrere anche lato front-end a soluzioni piu' generiche.

.. note:: Check sample code at:  (10) Front-end generic helpers to work with any Model


Generic urls
------------

Possiamo definire due end-point del tutto generici richiedento come paramteri
**app_label** e **model_name** per individuare il Model richiesto;
trattandosi di stringhe, possono essere inserite in un url:

file `frontend/urls.py`

.. code:: python

    urlpatterns = [
        ...
        # Edit any object
        path('object/<str:app_label>/<str:model_name>/add/', views.edit_object, name="object-add"),
        path('object/<str:app_label>/<str:model_name>/<uuid:pk>/change/', views.edit_object, name="object-change"),
    ]

dove la nuova view edit_object() si incarica di fornire a generic_edit_view() la ModelForm opportuna:

.. code:: python

    from .forms import get_model_form_class

    def edit_object(request, app_label, model_name, pk=None):
        model_form_class = get_model_form_class(app_label, model_name)
        return generic_edit_view(request, model_form_class, pk)

Il vero lavoro viene delegato all'utility get_model_form_class() che seleziona
la prima ModelForm compatibile con il Model richiesto, oppure ne crea una al volo:

file `frontend/forms.py`

.. code:: python

    import sys
    import inspect
    from django import forms
    from django.apps import apps


    def get_model_form_class(app_label, model_name):

        model_form_class = None

        # List all ModelForms in this module
        model_forms = [
            klass
            for name, klass in inspect.getmembers(sys.modules[__name__])
            if inspect.isclass(klass) and issubclass(klass, forms.ModelForm)
        ]

        # Scan ModelForms until we find the right one
        for model_form in model_forms:
            model = model_form._meta.model
            if (model._meta.app_label, model._meta.model_name) == (app_label, model_name):
                return model_form

        # Failing that, build a suitable ModelForm on the fly
        model_class = apps.get_model(app_label, model_name)
        class _ObjectForm(forms.ModelForm):
            class Meta:
                model = model_class
                exclude = []
        return _ObjectForm

Il template utilizzato per il rendering della pagina puo' utilizzare i nuovi urls generici,
nell'ipotesi che il context ricevuto sia stato annotato con la variabile **model**::

    {# change object #}
    data-action="{% url 'frontend:object-change' model|app_label model|model_name object.id %}"

    {# add object #}
    data-action="{% url 'frontend:object-add' model|app_label model|model_name %}"

Per estrarre **app_label** e **model_name** e altre informazioni "meta" da **model**
e' necessario predisporre alcuni semplici template_tags:

file `frontend/template_tags/frontend_tags.py`

.. code:: python

    from django import template
    from django.urls import reverse

    register = template.Library()


    @register.filter
    def model_verbose_name(model):
        """
        Sample usage:
            {{model|model_name}}
        """
        return model._meta.verbose_name


    @register.filter
    def model_verbose_name_plural(model):
        """
        Sample usage:
            {{model|model_name}}
        """
        return model._meta.verbose_name_plural


    @register.filter
    def model_name(model):
        """
        Sample usage:
            {{model|model_name}}
        """
        return model._meta.model_name


    @register.filter
    def app_label(model):
        """
        Sample usage:
            {{model|app_label}}
        """
        return model._meta.app_label


Per maggiore leggibilita' possiamo anche introdurre ulteriori filtri che
forniscono direttamente il link "canonico":

.. code:: python

    @register.filter
    def change_object_url(object):
        """
        Given an object, returns the "canonical" url for object editing:

            <a href="{{object|change_object_url}}">change this object</a>
        """
        model = object.__class__
        return reverse('frontend:object-change', args=(model._meta.app_label, model._meta.model_name, object.id))


    @register.filter
    def change_model_url(model, object_id):
        """
        Given a model and an object id, returns the "canonical" url for object editing:

            <a href="{{model|change_model_url:object.id}}">change this object</a>
        """
        return reverse('frontend:object-change', args=(model._meta.app_label, model._meta.model_name, object_id))


    @register.filter
    def add_model_url(model):
        """
        Given a model, return the "canonical" url for adding a new object:

            <a href="{{model|add_model_url}}">add a new object</a>
        """
        return reverse('frontend:object-add', args=(model._meta.app_label, model._meta.model_name))

e riscrivere il template piu' semplicemente come segue::

    {# change object #}
    data-action="{{model|change_model_url:object.id}}"

    {# add object #}
    data-action="{{model|add_model_url}}"

