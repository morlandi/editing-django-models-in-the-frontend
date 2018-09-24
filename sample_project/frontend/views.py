import time
from django.apps import apps
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from backend.models import Artist
from backend.models import Album
from backend.models import Song
from .utils import get_object_by_uuid_or_404
from .forms import get_model_form_class
from .forms import SimpleForm
from .forms import ArtistCreateForm
from .forms import ArtistUpdateForm
from .forms import AlbumEditForm


def about(request):
    # messages.success(request, 'test message (success)')
    # messages.info(request, 'test message (info)')
    # messages.warning(request, 'test message (warning)')
    # messages.error(request, 'test message (error)')
    return render(request, 'frontend/about.html', {
    })


def simple_content(request):
    return HttpResponse('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dignissim dapibus ipsum id elementum. Morbi in justo purus. Duis ornare lobortis nisl eget condimentum. Donec quis lorem nec sapien vehicula eleifend vel sit amet nunc.')


def simple_content_forbidden(request):
    raise PermissionDenied


def simple_content2(request):
    # Either render only the modal content, or a full standalone page
    if request.is_ajax():
        template_name = 'frontend/includes/simple_content2_inner.html'
    else:
        template_name = 'frontend/includes/simple_content2.html'
    return render(request, template_name, {
    })


def simple_form(request):
    if request.is_ajax():
        template_name = 'frontend/includes/simple_form_inner.html'
    else:
        template_name = 'frontend/includes/simple_form.html'

    if request.method == 'POST':
        time.sleep(1.0)
        form = SimpleForm(data=request.POST)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                messages.info(request, "Form has been validated" )
    else:
        form = SimpleForm()

    return render(request, template_name, {
        'form': form,
    })


@login_required
def artists(request):
    template_name = 'frontend/artists.html'
    return render(request, template_name, {
        'artists': Artist.objects.all()
    })


@login_required
def artists2(request):
    template_name = 'frontend/artists2.html'
    return render(request, template_name, {
        'artists': Artist.objects.all()
    })


@login_required
def artists_and_albums(request):
    template_name = 'frontend/artists_and_albums.html'
    return render(request, template_name, {
        'artists': Artist.objects.all(),
        'albums': Album.objects.all(),
    })


@login_required
def songs(request):
    template_name = 'frontend/songs.html'
    return render(request, template_name, {
        'model': Song,
        'objects': Song.objects.all(),
    })


################################################################################
# View to create a new Artist

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


################################################################################
# View to update an existing Artist

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


################################################################################
# Edit any object

def edit_object(request, app_label, model_name, pk=None):
    """
    Choose a suitable ModelForm class, than invoke generic_edit_view()
    """
    model_form_class = get_model_form_class(app_label, model_name)
    return generic_edit_view(request, model_form_class, pk)


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
