Creating and updating a Django Model in the front-end
=====================================================

We can now apply what we've built so far to edit a specific Django model
from the front-end.

.. note:: Check sample code at:  (7) Creating and updating a Django Model in the front-end


Creating a new model
--------------------

This is the view:

.. code:: python

    @login_required
    def artist_create(request):

        if not request.user.has_perm('backend.add_artist'):
            raise PermissionDenied

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend/includes/generic_form_inner.html'
        else:
            template_name = 'frontend/includes/generic_form.html'

        object = None
        if request.method == 'POST':
            form = ArtistCreateForm(data=request.POST)
            if form.is_valid():
                object = form.save()
                if not request.is_ajax():
                    # reload the page
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = ArtistCreateForm()

        return render(request, template_name, {
            'form': form,
            'object': object,
        })

and this is the form:

.. code:: python

    class ArtistCreateForm(forms.ModelForm):

        class Meta:
            model = Artist
            fields = [
                'description',
                'notes',
            ]

Note that we're using a generic template called `frontend/includes/generic_form_inner.html`;

Chances are we'll reuse it unmodified for other Models as well.

.. code:: html

    {% load i18n bootstrap3 %}

    <div class="row">
        <div class="col-sm-8">

            <form method="post" class="form" novalidate>
                {% csrf_token %}
                {% bootstrap_form form %}
                <input type="hidden" name="object_id" value="{{ object.id|default:'' }}">
                {% buttons %}
                    <div class="form-submit-row">
                        <button type="submit" class="btn btn-primary">
                            {% bootstrap_icon "star" %} {% trans 'Send' %}
                        </button>
                    </div>
                {% endbuttons %}
            </form>
        </div>
    </div>

On successful creation, we might want to update the user interface;
in the example, for simplicity, we just reload the entire page,
but before doing that we also display with an alert the new object id retrieved
from the hidden field 'object_id' of the form;
this could be conveniently used for in-place page updating.

.. code:: javascript

    <script language="javascript">

        function afterModalCreateSuccess(modal) {
            var object_id = modal.find('input[name=object_id]').val();
            alert('New artist created: id=' + object_id);
            location.reload(true);
        }

    </script>


Updating an existing object
---------------------------

We treat the update of an existing object in a similar fashion,
but binding the form to the specific database record.

The view:

.. code:: python

    @login_required
    def artist_update(request, pk):

        if not request.user.has_perm('backend.change_artist'):
            raise PermissionDenied

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend/includes/generic_form_inner.html'
        else:
            template_name = 'frontend/includes/generic_form.html'

        object = get_object_by_uuid_or_404(Artist, pk)
        if request.method == 'POST':
            form = ArtistUpdateForm(instance=object, data=request.POST)
            if form.is_valid():
                form.save()
                if not request.is_ajax():
                    # reload the page
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = ArtistUpdateForm(instance=object)

        return render(request, template_name, {
            'object': object,
            'form': form,
        })

and the form:

.. code:: python

    class ArtistUpdateForm(forms.ModelForm):

        class Meta:
            model = Artist
            fields = [
                'description',
                'notes',
            ]

Finally, here's the object id retrival after successful completion:

.. code:: javascript

    <script language="javascript">

        function afterModalUpdateSuccess(modal) {
            var object_id = modal.find('input[name=object_id]').val();
            alert('Artist updated: id=' + object_id);
            location.reload(true);
        }

    </script>

Possible optimizations
----------------------

In the code above, we can detect at list three redundancies:

- the two model forms are identical
- the two views are similar
- and, last but not least, we might try to generalize the views for reuse with any Django model

We'll investigate all these opportunities later on; nonetheless, it's nice to
have a simple snippet available for copy and paste to be used as a starting point
anytime a specific customization is in order.
