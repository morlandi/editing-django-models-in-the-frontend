from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from . import forms

app_name = 'frontend'


urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html"), name="index"),
    path('about/', views.about, name="about"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='logout'),

    path('basic-modal/',
        TemplateView.as_view(template_name="frontend/basic_modal.html"),
        name="basic-modal"),
    path('basic-modal-which-returns-a-value/',
        TemplateView.as_view(template_name="frontend/basic_modal_which_returns_a_value.html"),
        name="basic-modal-which-returns-a-value"),
    path('basic-modal-with-bootstrap3/',
        TemplateView.as_view(template_name="frontend/basic_modal_with_bootstrap3.html"),
        name="basic-modal-with-bootstrap3"),
    path('generic-empty-modal-for-django/',
        TemplateView.as_view(template_name="frontend/generic_empty_modal_for_django.html"),
        name="generic-empty-modal-for-django"),
    path('modal-with-simple-content/',
        TemplateView.as_view(template_name="frontend/modal_with_simple_content.html"),
        name="modal-with-simple-content"),
    path('modal-with-form/',
        TemplateView.as_view(template_name="frontend/modal_with_form.html"),
        name="modal-with-form"),

    path('artists/', views.artists, name="artists"),
    path('artists2/', views.artists2, name="artists2"),
    path('artists_and_albums/', views.artists_and_albums, name="artists-and-albums"),

    path('simple-content', views.simple_content, name="simple-content"),
    path('simple-content-forbidden', views.simple_content_forbidden, name="simple-content-forbidden"),
    path('simple-content2', views.simple_content2, name="simple-content2"),
    path('simple-form', views.simple_form, name="simple-form"),
    path('artist/create/', views.artist_create, name="artist-create"),
    path('artist/<uuid:pk>/update/', views.artist_update, name="artist-update"),

    path('artist/add/', views.artist_edit, name="artist-add"),
    path('artist/<uuid:pk>/change/', views.artist_edit, name="artist-change"),

    path('album/add/',
        views.generic_edit_view,
        {'model_form_class': forms.AlbumEditForm},
        name="album-add"),
    path('album/<uuid:pk>/change/',
        views.generic_edit_view,
        {'model_form_class': forms.AlbumEditForm}, name="album-change"),
]
