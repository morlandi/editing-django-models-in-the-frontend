Basic modals with Django
========================

Purpose
-------

Spostando la nostra attenzione su un sito dinamico basato su Django, i nostri
obiettivi principali diventano:

- disporre di una dialog box da usare come "contenitore" per l'interazione
  con l'utente, e il cui layout sia coerente con la grafica del front-end
- il contenuto della dialog e il ciclo di vita dell'interazione con l'utente
  viene invece definito e gestito "lato server"
- la dialog viene chiusa una volta che l'utente completato (o annullato)
  l'operazione

Display the empty dialog
------------------------

Il layout di ciascuna dialog box (quindi l'intera finestra a meno del contenuto)
viene descritto in un template, e il rendering grafico viene determinato da un
unico foglio di stile comune a tutte le finestre (file "modals.css").

.. note:: Check sample code at: (4) A generic empty modal for Django" illustra diverse possibilita'

Nel caso piu' semplice, ci limitiamo a visualizare la dialog prevista dal
template::

    <a href=""
       onclick="openModalDialog(event, '#modal_generic'); return false;">
        <i class="fa fa-keyboard-o"></i> Open generic modal (no contents, no customizations)
    </a>

.. figure:: /_static/images/empty_modal.png

   w3school modal example

Questo e' sufficiente nei casi in cui il template contenga gia' tutti gli
elementi richiesti; ci sono pero' buone possibilita' che un'unica "generica" dialog
sia riutilizzabile in diverse circostanze (o forse ovunque) pur di fornire un
minimo di informazioni accessorie:

.. code:: html

    <a href=""
       data-dialog-class="modal-lg"
       data-title="Set value"
       data-subtitle="Insert the new value to be assigned to the Register"
       data-icon="fa-keyboard-o"
       data-button-save-label="Save"
       onclick="openModalDialog(event, '#modal_generic'); return false;">
        <i class="fa fa-keyboard-o"></i> Open generic modal (no contents)
    </a>

.. figure:: /_static/images/empty_modal_customized.png

In entrambi i casi si fa' riperimento a un semplice javascript helper, che
provvede ad aggiornare gli attributi della dialog prima di visualizzarla,
dopo avere reperito i dettagli dall'elemento che l'ha invocata;
il vantaggio di questo approccio e' che possiamo definire questi dettagli
nel template della pagina principale, e quindi utilizzandone il contesto:

.. code:: javascript

    <script language="javascript">

        function initModalDialog(event, modal_element) {
            /*
                You can customize the modal layout specifing optional "data" attributes
                in the element (either <a> or <button>) which triggered the event;
                "modal_element" identifies the modal HTML element.

                Sample call:

                <a href=""
                   data-title="Set value"
                   data-subtitle="Insert the new value to be assigned to the Register"
                   data-dialog-class="modal-lg"
                   data-icon="fa-keyboard-o"
                   data-button-save-label="Save"
                   onclick="openModalDialog(event, '#modal_generic'); return false;">
                    <i class="fa fa-keyboard-o"></i> Open generic modal (no contents)
                </a>
            */
            var modal = $(modal_element);
            var target = $(event.target);

            var title = target.data('title') || '';
            var subtitle = target.data('subtitle') || '';
            // either "modal-lg" or "modal-sm" or nothing
            var dialog_class = (target.data('dialog-class') || '') + ' modal-dialog';
            var icon_class = (target.data('icon') || 'fa-laptop') + ' fa modal-icon';
            var button_save_label = target.data('button-save-label') || 'Save changes';

            modal.find('.modal-dialog').attr('class', dialog_class);
            modal.find('.modal-title').text(title);
            modal.find('.modal-subtitle').text(subtitle);
            modal.find('.modal-header .title-wrapper i').attr('class', icon_class);
            modal.find('.modal-footer .btn-save').text(button_save_label);
            modal.find('.modal-body').html('');

            // Annotate with target (just in case)
            modal.data('target', target);

            return modal;
        }

        function openModalDialog(event, modal_element) {
            var modal = initModalDialog(event, modal_element);
            modal.modal('show');
        }

    </script>


Make the modal draggable
------------------------

To have the modal draggable, you can specify the "draggable" class::

    <div class="modal draggable" id="modal_generic" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog">
          ...

and add this statement at the end of initModalDialog()::

    if (modal.hasClass('draggable')) {
        modal.find('.modal-dialog').draggable({
            handle: '.modal-header'
        });
    }

.. warning:: draggable() requires the inclusion of jQuery UI

It's usefull to give a clue to the user adding this style::

    .modal.draggable .modal-header {
        cursor: move;
    }


Organizzazione dei files
------------------------

Per convenienza, tutti i templates relativi alle dialog (quello generico e le
eventuali varianti specializzate) vengono memorizzate in un unico folder:

    `templates/frontent/modals`

e automaticamente incluse nel template "base.html":

.. code:: html

    {% block modals %}
        {% include 'frontend/modals/generic.html' %}
        {% include 'frontend/modals/dialog1.html' %}
        {% include 'frontend/modals/dialog2.html' %}
        ...
    {% endblock modals %}

Questo significa che tutte le modal dialogs saranno disponibili in qualunque pagina,
anche quando non richieste; trattandosi di elementi non visibili della pagina,
non ci sono particolari controindicazioni; nel caso, il template specifico puo'
eventulmente ridefinire il blocco `{% block modals %}` ed includere i soli template
effettivamente necessari.

Altri files utilizzati:

- `static/frontend/css/modals.css`: stili comuni a tutte le dialogs
- `static/frontend/js/modals.js`: javascript helpers pertinenti alla gestione delle dialogs
