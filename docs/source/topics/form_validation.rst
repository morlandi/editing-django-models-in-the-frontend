Form validation in the modal
============================

We've successfully injected data retrieved from the server in our modals,
but did not really interact with the user yet.

When the modal body contains a form, things start to become interesting and tricky.

Handling form submission
------------------------

First and foremost, we need to **prevent the form from performing its default submit**.

If not, after submission we'll be redirected to the form action, outside the context
of the dialog.

We'll do this binding to the form's submit event, where we'll serialize the form's
content and sent it to the view for validation via an Ajax call.

Then, upon a successufull response from the server, **we'll need to further investigate
the HTML received**:

- if it contains any field error, the form did not validate successfully,
  so we update the modal body with the new form and its errors

- otherwise, user interaction is completed, and we can finally close the modal


We'll obtain all this (and more) with a javacript helper function **formAjaxSubmit()**
which I'll explain later in details.

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
                formAjaxSubmit(modal, url, null, null);
            }).fail(function(jqXHR, textStatus, errorThrown) {
                alert("SERVER ERROR: " + errorThrown);
            });
        }

    </script>


.. figure:: /_static/images/form_validation_1.png
   :scale: 80 %

   A form in the modal dialog

.. figure:: /_static/images/form_validation_2.png
   :scale: 80 %

   While the form does not validate, we keep the dialog open

Again, the very same view can also be used to render a standalone page:

.. figure:: /_static/images/form_standalone.png


The formAjaxSubmit() helper
---------------------------

I based my work on the inspiring ideas presented in this brilliant article:

`Use Django's Class-Based Views with Bootstrap Modals <https://dmorgan.info/posts/django-views-bootstrap-modals/>`_

Here's the full code:

.. code:: javascript

    <script language="javascript">

        function formAjaxSubmit(modal, action, cbAfterLoad, cbAfterSuccess) {
            var form = modal.find('.modal-body form');
            var header = $(modal).find('.modal-header');

            // use footer save button, if available
            var btn_save = modal.find('.modal-footer .btn-save');
            if (btn_save) {
                modal.find('.modal-body form .form-submit-row').hide();
                btn_save.off().on('click', function(event) {
                    modal.find('.modal-body form').submit();
                });
            }
            if (cbAfterLoad) { cbAfterLoad(modal); }

            // Give focus to first visible form field
            modal.find('form input:visible').first().focus();

            // bind to the form’s submit event
            $(form).on('submit', function(event) {

                // prevent the form from performing its default submit action
                event.preventDefault();
                header.addClass('loading');

                var url = $(this).attr('action') || action;

                // serialize the form’s content and send via an AJAX call
                // using the form’s defined action and method
                $.ajax({
                    type: $(this).attr('method'),
                    url: url,
                    data: $(this).serialize(),
                    success: function(xhr, ajaxOptions, thrownError) {

                        // If the server sends back a successful response,
                        // we need to further check the HTML received

                        // update the modal body with the new form
                        $(modal).find('.modal-body').html(xhr);

                        // If xhr contains any field errors,
                        // the form did not validate successfully,
                        // so we keep it open for further editing
                        if ($(xhr).find('.has-error').length > 0) {
                            formAjaxSubmit(modal, url, cbAfterLoad, cbAfterSuccess);
                        } else {
                            // otherwise, we've done and can close the modal
                            $(modal).modal('hide');
                            if (cbAfterSuccess) { cbAfterSuccess(modal); }
                        }
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                        console.log('SERVER ERROR: ' + thrownError);
                    },
                    complete: function() {
                        header.removeClass('loading');
                    }
                });
            });
        }

    </script>


As anticipated, the most important action is to hijack form submission::

    // bind to the form’s submit event
    $(form).on('submit', function(event) {

        // prevent the form from performing its default submit action
        event.preventDefault();
        header.addClass('loading');

        var url = $(this).attr('action') || action;

        // serialize the form’s content and sent via an AJAX call
        // using the form’s defined action and method
        $.ajax({
            type: $(this).attr('method'),
            url: url,
            data: $(this).serialize(),
            ...

If the form specifies an action, we use it as the end-point of the ajax call;
if not (which is the most common case), we're using the same view for both
rendering and form processing, and we can reuse the original url instead::

    var url = $(this).attr('action') || action;

Secondly, we need to detect any form errors after submission; see the "success"
callback after the Ajax call for details.

Finally, we need to take care of the submit button embedded in the form.

While it's useful and necessary for the rendering of a standalone page, it's
rather disturbing in the modal dialog:

.. figure:: /_static/images/form_validation_extra_button.png
   :scale: 80 %

   Can we hide the "Send" button and use the "Save" button from the footer instead ?

Here's the relevant code::

    // use footer save button, if available
    var btn_save = modal.find('.modal-footer .btn-save');
    if (btn_save) {
        modal.find('.modal-body form .form-submit-row').hide();
        btn_save.off().on('click', function(event) {
            modal.find('.modal-body form').submit();
        });
    }

During content loading, we add a "loading" class to the dialog header,
to make a spinner icon visible until we're ready to either update or close the modal.


Optional callbacks supported by formAjaxSubmit()
------------------------------------------------

    cbAfterLoad
        called every time new content has been loaded;
        you can use it to bind form controls when required

    cbAfterSuccess
        called after successfull submission; at this point the modal
        has been closed, but the bounded form might still contain useful informations
        that you can grab for later inspection

Sample usage::

    ...
    formAjaxSubmit(modal, url, afterModalLoad, afterModalSuccess);
    ...

    function afterModalLoad(modal) {
        console.log('modal %o loaded', modal);
    }

    function afterModalSuccess(modal) {
        console.log('modal %o succeeded', modal);
    }


.. note:: Check sample code at:  (6) Form validation in the modal

.. warning:: In the sample project, a sleep of 1 sec has been included in the view (POST) to simulate a more complex elaboration which might occur in real situations
