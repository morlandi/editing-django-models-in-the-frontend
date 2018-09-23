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

        <a href="{{object|change_object_url}}">change this object</a></br />
    """
    model = object.__class__
    return reverse('frontend:object-change', args=(model._meta.app_label, model._meta.model_name, object.id))


@register.filter
def change_model_url(model, object_id):
    """
    Given a model and an object id, returns the "canonical" url for object editing:

        <a href="{{model|change_model_url:object.id}}">change this object</a></br />
    """
    return reverse('frontend:object-change', args=(model._meta.app_label, model._meta.model_name, object_id))


@register.filter
def add_model_url(model):
    """
    Given a model, return the "canonical" url for adding a new object:

        <a href="{{model|add_model_url}}">add a new object</a></br />
    """
    return reverse('frontend:object-add', args=(model._meta.app_label, model._meta.model_name))
