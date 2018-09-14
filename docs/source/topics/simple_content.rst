Modals with simple content
==========================

Possiamo riempire il contenuto della dialog invocando via Ajax una vista che
restituisca l'opportuno frammento HTML:

.. code:: javascript

    <script language="javascript">

        function openMyModal(event) {
            var modal = initModalDialog(event, '#modal_generic');
            var url = $(event.target).data('action');
            modal.find('.modal-body').load(url, function() {
                modal.modal('show');
            });
        }

    </script>

.. code:: python

    def simple_content(request):
        return HttpResponse('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dignissim dapibus ipsum id elementum. Morbi in justo purus. Duis ornare lobortis nisl eget condimentum. Donec quis lorem nec sapien vehicula eleifend vel sit amet nunc.')

.. figure:: /_static/images/modal_with_simple_content_1.png

Si osservi come abbiamo specificato l'url della view remota nell'attributo
"data-action" del trigger.

Un limite di questa semplice soluzione e' che non siamo in grado di rilevare
eventuali errori del server, e quindi in caso di errore la dialog verrebbe comunque
aperta (con contenuto vuoto).

Il problema viene facilmente superato invocando direttamente $.ajax() anziche'
lo shortcut load().

La soluzione e' leggermente piu' verbose, ma consente un controllo piu' accurrato:

.. code:: javascript

    <script language="javascript">

        function openMyModal(event) {
            var modal = initModalDialog(event, '#modal_generic');
            var url = $(event.target).data('action');
            $.ajax({
                type: "GET",
                url: url
            }).done(function(data, textStatus, jqXHR) {
                modal.find('.modal-body').html(data);
                modal.modal('show');
            }).fail(function(jqXHR, textStatus, errorThrown) {
                alert("SERVER ERROR: " + errorThrown);
            });
        }

    </script>

.. code:: python

    def simple_content_forbidden(request):
        raise PermissionDenied

.. figure:: /_static/images/server_error_detected.png

More flexible server side processing
------------------------------------

A volte puo' essere utile riutilizzare la stessa view per fornire, a seconda delle
circostanze, una dialog modale oppure una pagina standalone.

La soluzione proposta prevede l'utilizzo di templates differenziati nei due casi:

.. code:: python

    def simple_content2(request):

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend/includes/simple_content2_inner.html'
        else:
            template_name = 'frontend/includes/simple_content2.html'

        return render(request, template_name, {
        })

dove il template "inner" fornisce il contenuto:

.. code:: html

    <div class="row">
        <div class="col-sm-4">
            {% lorem 1 p random %}
        </div>
        <div class="col-sm-4">
            {% lorem 1 p random %}
        </div>
        <div class="col-sm-4">
            {% lorem 1 p random %}
        </div>
    </div>

mentre il template "esterno" si limita a includerlo nel contesto piu' completo
previsto dal frontend:

.. code:: html

    {% extends "base.html" %}
    {% load static staticfiles i18n %}

    {% block content %}
    {% include 'frontend/includes/simple_content2_inner.html' %}
    {% endblock content %}

.. figure:: /_static/images/modal_with_simple_content_2.png
   :scale: 80 %

   Modal dialog

.. figure:: /_static/images/modal_with_simple_content_2_standalone.png

   Same content in a standalone page


.. note:: Check sample code at:  (5) Modal with simple content

