# ADMIN PAGE URL

from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name: str = "visualboard"
urlpatterns = [
    path("base",      TemplateView.as_view(template_name="visualboard/index.html"), name="base"),
    path("register/", views.AdminRegisterView.as_view(), name="register"),
    path("login/",    views.AdminLoginView.as_view(), name="login"),
    path("logout/",   views.logout_view, name="logout")
]

