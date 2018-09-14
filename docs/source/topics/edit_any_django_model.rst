A fully generic solution for Django models editing in the front-end
===================================================================

We're really very close to **the Holy Grail of Django models editing in the front-end**.

Can we really do it all with a single generic view ?

Yes sir !

.. note::  Check sample code at: (9) A fully generic solution for Django models editing in the front-end

.. code:: python

    ################################################################################
    # A fully generic "edit" view to either create a new object or update an existing one;
    # works with any Django model

    def generic_edit_view(request, model_form_class, pk=None):

        model_class = model_form_class._meta.model
        app_label = model_class._meta.app_label
        model_name = model_class._meta.model_name
        model_verbose_name = model_class._meta.verbose_name.capitalize()

        # Retrieve object
        if pk is None:
            # "Add" mode
            object = None
            required_permission = '%s.add_%s' % (app_label, model_name)
        else:
            # Change mode
            object = get_object_by_uuid_or_404(model_class, pk)
            required_permission = '%s.change_%s' % (app_label, model_name)

        # Check user permissions
        if not request.user.is_authenticated or not request.user.has_perm(required_permission):
            raise PermissionDenied

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend/includes/generic_form_inner.html'
        else:
            template_name = 'frontend/includes/generic_form.html'

        if request.method == 'POST':
            form = model_form_class(instance=object, data=request.POST)
            if form.is_valid():
                object = form.save()
                if not request.is_ajax():
                    # reload the page
                    if pk is None:
                        message = 'The %s "%s" was added successfully.' % (model_verbose_name, object)
                    else:
                        message = 'The %s "%s" was changed successfully.' % (model_verbose_name, object)
                    messages.success(request, message)
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = model_form_class(instance=object)

        return render(request, template_name, {
            'object': object,
            'form': form,
        })

Adding an appropriate ModelForm in the URL pattern is all what we need;
from that, the view will deduce the Model and other related details.

.. code:: python

    urlpatterns = [
        ...
        path('album/add/',
            views.generic_edit_view,
            {'model_form_class': forms.AlbumEditForm},
            name="album-add"),
        path('album/<uuid:pk>/change/',
            views.generic_edit_view,
            {'model_form_class': forms.AlbumEditForm},
            name="album-change"),
        ...
    ]

In the page template, we bind the links to the views as follows:

.. code:: html

    <!-- Change -->
    <a href=""
       data-action="{% url 'frontend:album-change' row.id %}"
       onclick="onObjectEdit(event, null, afterObjectEditSuccess); return false;"
       data-title="Change album: {{ row }}"
    >
        <i class="fa fa-edit"></i> Edit
    </a>

    ...

    <!-- Add -->
    <button
        href=""
        data-action="{% url 'frontend:album-add' %}"
        data-title="New album"
        onclick="onObjectEdit(event, null, afterObjectEditSuccess); return false;"
        type="button"class="btn btn-primary">
        New
    </button>

.. figure:: /_static/images/holy_grail_1.png

.. figure:: /_static/images/holy_grail_2.png
