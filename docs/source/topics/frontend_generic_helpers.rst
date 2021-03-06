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

Se il front-end prevede un numero limitato di Models, e' ragionevole accettare queste ripetizioni;
in caso contrario puo' essere giustificato affrontare la complicazione di introdurre anche lato
front-end soluzioni piu' generiche.

.. note:: Check sample code at:  (10) Front-end generic helpers to work with any Model


Generic end-points for changing and adding an object
----------------------------------------------------

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
nell'ipotesi che il context ricevuto sia stato annotato allo scopo con la variabile **model**::

    {# change object #}
    data-action="{% url 'frontend:object-change' model|app_label model|model_name object.id %}"

    {# add object #}
    data-action="{% url 'frontend:object-add' model|app_label model|model_name %}"

Sfortunatamente per estrarre **app_label** e **model_name** e altre informazioni accessorie
da **model** e' necessario predisporre alcuni semplici template_tags, poiche'
l'attributo `_meta` del model non e' direttamente accessibile nel contesto del template:

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
    def add_model_url(model):
        """
        Given a model, return the "canonical" url for adding a new object:

            <a href="{{model|add_model_url}}">add a new object</a>
        """
        return reverse('frontend:object-add', args=(model._meta.app_label, model._meta.model_name))


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


e riscrivere il template piu' semplicemente come segue::

    {# add object #}
    data-action="{{model|add_model_url}}"

    {# change object #}
    data-action="{{model|change_model_url:object.id}}"

    oppure:

    {# change object #}
    data-action="{{object|change_object_url}}"


Deleting an object
------------------

.. figure:: /_static/images/objects_table.png

Associamo all'url::

    path('object/<str:app_label>/<str:model_name>/<uuid:pk>/delete/', views.delete_object, name="object-delete"),

una view responsabile di eseguire la cancellazione di un generico oggetto:

.. code:: python

    ################################################################################
    # Deleting an object

    def delete_object(request, app_label, model_name, pk):

        required_permission = '%s.delete_%s' % (app_label, model_name)
        if not request.user.is_authenticated or not request.user.has_perm(required_permission):
            raise PermissionDenied

        model = apps.get_model(app_label, model_name)
        object = get_object_by_uuid_or_404(model, pk)
        object_id = object.id
        object.delete()

        return HttpResponse(object_id)

Verra' invocata via Ajax da una funzione javascript accessoria che chiede preventivamente
la conferma dell'utente:


.. code:: javascript

    function confirmRemoteAction(url, title, afterObjectDeleteCallback) {
        var modal = $('#modal_confirm');
        modal.find('.modal-title').text(title);
        modal.find('.btn-yes').off().on('click', function() {
            // User selected "Yes", so proceed with remote call
            $.ajax({
                type: 'GET',
                url: url
            }).done(function(data) {
                if (afterObjectDeleteCallback) {
                    afterObjectDeleteCallback(data);
                }
            }).fail(function(jqXHR, textStatus, errorThrown) {
                alert('SERVER ERROR: ' + errorThrown);
            });
        });
        modal.modal('show');
    }

e quindi, nel template::

    <a href=""
       onclick="confirmRemoteAction('{{object|delete_object_url}}', 'Deleting {{object}}', afterObjectDelete); return false;">
        <i class="fa fa-eraser"></i> Delete
    </a>

La callback opzionale **afterObjectDelete()** viene invocata dopo l'effettiva cancellazione,
ricevendo l'id dell'oggetto eliminato.

Nel progetto d'esempio, per semplicita', si limita a ricaricare la pagina,
mentre in casi applicativi reali verra' convenientemente utilizzata
per aggiornare "chirurgicamente" la pagina esistente.


.. figure:: /_static/images/confirm_deletion.png
   :scale: 80 %

Cloning an object
-----------------

La possibilita' di duplicare un oggetto esistente, normalmente non prevista dalla
interfaccia di amministrazione di Django, e' molto interessante in applicazioni
fortemente orientate alla gestione dati, perche' consente all'utilizzatore un
notevole risparmio di tempo quando e' richiesto l'interimento di dati ripetitivi.

In sostanza consente di fornire caso per caso valori di default "opportuni" in modo arbitrario.

Possiamo predisporre una view che duplica un oggetto esistente analogamente a
quanto gia' fatto per la cancellazione:

.. code:: python

    ################################################################################
    # Cloning an object

    def clone_object(request, app_label, model_name, pk):

        required_permission = '%s.add_%s' % (app_label, model_name)
        if not request.user.is_authenticated or not request.user.has_perm(required_permission):
            raise PermissionDenied

        model = apps.get_model(app_label, model_name)
        object = get_object_by_uuid_or_404(model, pk)
        new_object = object.clone(request)
        return HttpResponse(new_object.id)

Qui stiamo supponendo che il Model metta a disposizione un opportuno metodo **clone()**;
conviene delegare questa attivita' allo specifico Model, che si preoccupera'
di gestire opportunamente le proprie eventuali relazioni M2M, ed eseguire eventuali
elaborazioni accessorie (rinumerazione del campo `position`, etc):

.. code:: python


    class Song(BaseModel):

        ...

        def clone(self, request=None):

            if request and not request.user.has_perm('backend.add_song'):
                raise PermissionDenied

            obj = Song.objects.get(id=self.id)
            obj.pk = uuid.uuid4()
            obj.description = increment_revision(self.description)
            obj.save()
            return obj

.. warning:: Supply a default generic clone procedure when the Model doesn't provide it's own

Per duplicare anche le eventuali relazioni, vedere:

https://docs.djangoproject.com/en/1.10/topics/db/queries/#copying-model-instances


La stessa funzione javascript confirmRemoteAction() utilizzata in precedenza puo' essere
invocata anche qui per richiedere la conferma dell'utente prima dell'esecuzione::

    <a href=""
       onclick="confirmRemoteAction('{{object|clone_object_url}}', 'Duplicating {{object}}', afterObjectClone); return false;">
        <i class="fa fa-clone"></i> Duplicate
    </a>

La callback **afterObjectClone()** riceve l'id dell'oggetto creato.


Checking user permissions
-------------------------

Tutte le viste utilizzate sin qui per manipolare i Models sono gia' protette in
termine di permissions accordate all'utente; in caso di violazione, viene lanciata l'eccezione PermissionDenied, e il front-end
visualizza un server error.

In alternativa, possiamo inibire o nascondere i controlli di editing dalla pagina
quanto l'utente loggato non e' autorizzato alle operazioni.

Il seguente template tag consente di verificare se l'utente e' autorizzato o meno
ad eseguire le azioni:

- add
- change
- delete
- view (Django >= 2.1 only)

.. code:: python

    @register.simple_tag(takes_context=True)
    def testhasperm(context, model, action):
        """
        Returns True iif the user have the specified permission over the model.
        For 'model', we accept either a Model class, or a string formatted as "app_label.model_name".
        """
        user = context['request'].user
        if isinstance(model, str):
            app_label, model_name = model.split('.')
        else:
            app_label = model._meta.app_label
            model_name = model._meta.model_name
        required_permission = '%s.%s_%s' % (app_label, action, model_name)
        return user.is_authenticated and user.has_perm(required_permission)

e puo' essere utilizzata assegnato il valore calcolato ad una variabile
per i successivi test::

    {% testhasperm model 'view' as can_view_objects %}
    {% if not can_view_objects %}
        <h2>Sorry, you have no permission to view these objects</h2>
    {% endif %}

Un'altra possibilita' e' quella di utilizzare un template tag "ishasperm" per
condizionare l'inclusione del controllo::

    {% ifhasperm model 'change' %}
        <a href=""
           data-action="{{model|change_model_url:object.id}}"
           onclick="openModalDialogWithForm(event, '#modal_generic', null, afterObjectChangeSuccess); return false;"
           data-title="Update {{ model|model_verbose_name }}: {{ object }}">
            <i class="fa fa-edit"></i> Edit
        </a>
        |
    {% endifhasperm %}

dove:

.. code:: python

    @register.tag
    def ifhasperm(parser, token):
        """
        Check user permission over specified model.
        (You can specify either a model or an object).
        """

        # Separating the tag name from the parameters
        try:
            tag, model, action = token.contents.split()
        except (ValueError, TypeError):
            raise template.TemplateSyntaxError(
                "'%s' tag takes three parameters" % tag)

        default_states = ['ifhasperm', 'else']
        end_tag = 'endifhasperm'

        # Place to store the states and their values
        states = {}

        # Let's iterate over our context and find our tokens
        while token.contents != end_tag:
            current = token.contents
            states[current.split()[0]] = parser.parse(default_states + [end_tag])
            token = parser.next_token()

        model_var = parser.compile_filter(model)
        action_var = parser.compile_filter(action)
        return CheckPermNode(states, model_var, action_var)


    class CheckPermNode(template.Node):
        def __init__(self, states, model_var, action_var):
            self.states = states
            self.model_var = model_var
            self.action_var = action_var

        def render(self, context):

            # Resolving variables passed by the user
            model = self.model_var.resolve(context)
            action = self.action_var.resolve(context)

            # Check user permission
            if testhasperm(context, model, action):
                html = self.states['ifhasperm'].render(context)
            else:
                html = self.states['else'].render(context) if 'else' in self.states else ''

            return html

.. figure:: /_static/images/check_user_permissions.png

