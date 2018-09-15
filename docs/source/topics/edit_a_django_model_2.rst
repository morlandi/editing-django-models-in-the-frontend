Creating and updating a Django Model in the front-end (optimized)
=================================================================

Let's start our optimizations by removing some redundancies.

.. note:: Check sample code at:  (8) Editing a Django Model in the front-end, using a common basecode for creation and updating

Sharing a single view for both creating a new specific Model and updating
an existing one is now straitforward; see `artist_edit()` belows:

.. code:: python

    ################################################################################
    # A single "edit" view to either create a new Artist or update an existing one

    def artist_edit(request, pk=None):

        # Retrieve object
        if pk is None:
            # "Add" mode
            object = None
            required_permission = 'backend.add_artist'
        else:
            # Change mode
            object = get_object_by_uuid_or_404(Artist, pk)
            required_permission = 'backend.change_artist'

        # Check user permissions
        if not request.user.is_authenticated or not request.user.has_perm(required_permission):
            raise PermissionDenied

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend/includes/generic_form_inner.html'
        else:
            template_name = 'frontend/includes/generic_form.html'

        if request.method == 'POST':
            form = ArtistUpdateForm(instance=object, data=request.POST)
            if form.is_valid():
                object = form.save()
                if not request.is_ajax():
                    # reload the page
                    if pk is None:
                        message = 'The object "%s" was added successfully.' % object
                    else:
                        message = 'The object "%s" was changed successfully.' % object
                    messages.success(request, message)
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = ArtistUpdateForm(instance=object)

        return render(request, template_name, {
            'object': object,
            'form': form,
        })

When "pk" is None, we switch to `add` mode, otherwise we retrieve the corresponding
object to `change` it.

Both "add" and "change" URL patterns point to the same view,
but the first one doesn’t capture anything from the URL and the default value
of None will be used for `pk`.

.. code:: python

    urlpatterns = [
        ...
        path('artist/add/', views.artist_edit, name="artist-add"),
        path('artist/<uuid:pk>/change/', views.artist_edit, name="artist-change"),
        ...
    ]

We also share a common form:

.. code:: python

    class ArtistEditForm(forms.ModelForm):
        """
        To be used for both creation and update
        """

        class Meta:
            model = Artist
            fields = [
                'description',
                'notes',
            ]

The javascript handler which opens the dialog can be refactored in a completely generic
way, with no reference to the specific Model in use (and is also reusable for
any dialog which submits an arbitrary form):

.. code:: javascript

    <script language="javascript">

        function openModalDialogWithForm(event, modal, cbAfterLoad, cbAfterSuccess) {
            // If "modal" is a selector, initialize a modal object,
            // otherwise just use it
            if ($.type(modal) == 'string') {
                modal = initModalDialog(event, modal);
            }

            var url = $(event.target).data('action');
            if (!url) {
                console.log('ERROR: openModalDialogWithForm() could not retrieve action from event');
                return;
            }

            $.ajax({
                type: 'GET',
                url: url
            }).done(function(data, textStatus, jqXHR) {
                modal.find('.modal-body').html(data);
                modal.modal('show');
                formAjaxSubmit(modal, url, cbAfterLoad, cbAfterSuccess);
            }).fail(function(jqXHR, textStatus, errorThrown) {
                alert('SERVER ERROR: ' + errorThrown);
            });
        }

    </script>

so I moved it from the template to "modals.js". It can be invoked directly from
there, or copied to any local template for further customization.


