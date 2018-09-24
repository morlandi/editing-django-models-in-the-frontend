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


@register.filter
def delete_object_url(object):
    """
    Given an object, returns the "canonical" url for object deletion:

        <a href="{{object|delete_object_url}}">delete this object</a>
    """
    model = object.__class__
    return reverse('frontend:object-delete', args=(model._meta.app_label, model._meta.model_name, object.id))


@register.filter
def delete_model_url(model, object_id):
    """
    Given a model and an object id, returns the "canonical" url for object deletion:

        <a href="{{model|delete_model_url:object.id}}">delete this object</a>
    """
    return reverse('frontend:object-delete', args=(model._meta.app_label, model._meta.model_name, object_id))


@register.filter
def clone_object_url(object):
    """
    Given an object, returns the "canonical" url for object cloning:

        <a href="{{object|clone_object_url}}">clone this object</a>
    """
    model = object.__class__
    return reverse('frontend:object-clone', args=(model._meta.app_label, model._meta.model_name, object.id))


@register.filter
def clone_model_url(model, object_id):
    """
    Given a model and an object id, returns the "canonical" url for object cloning:

        <a href="{{model|clone_model_url:object.id}}">clone this object</a>
    """
    return reverse('frontend:object-clone', args=(model._meta.app_label, model._meta.model_name, object_id))
