from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.caja, name="caja"),
    path("agregar/<int:producto_id>/", views.agregar, name="agregar"),
    path("cancelar/", views.cancelar, name="cancelar"),
    path("cobrar/", views.cobrar, name="cobrar"),
    path("login/", auth_views.LoginView.as_view(template_name="pedidos/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]